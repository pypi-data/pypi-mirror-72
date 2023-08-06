# Licensed under GNU General Public License v3 or later, see COPYING.
# Copyright (c) 2019 Red Hat, Inc., see CONTRIBUTORS.

import hashlib
import http.server
import os
import shutil
import socketserver
import threading
import time

import requests
import requests_mock
import cachecontrol
import cachecontrol.caches

from fingertip.util import path, log


OFFLINE = os.getenv('FINGERTIP_OFFLINE', '0') != '0'
BIG = 2**30  # too big for caching
STRIP_IF_OFFLINE = ('Cache-Control', 'Pragma')
STRIP_ALWAYS = ('TE', 'Transfer-Encoding', 'Keep-Alive', 'Trailer', 'Upgrade',
                'Connection', 'Host', 'Accept')
STRIP_HEADERS = STRIP_ALWAYS + STRIP_IF_OFFLINE if OFFLINE else STRIP_ALWAYS


class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


class HTTPCache:
    def __init__(self, host='127.0.0.1', port=0):
        self.host = host
        self._mocks = []
        self._local_files_to_serve = {}
        http_cache = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'

            def _status_and_headers(self, status_code, headers):
                self.send_response(status_code)
                for k, v in headers.items():
                    self.send_header(k, v)
                self.end_headers()

            def _serve(self, uri, headers, meth='GET'):  # caching proxy
                sess = http_cache._get_requests_session()
                basename = os.path.basename(uri)

                headers = {k: v for k, v in headers.items() if
                           not (k in STRIP_HEADERS or k.startswith('Proxy-'))}
                headers['Accept-Encoding'] = 'identity'
                log.debug(f'{meth} {basename} ({uri})')
                for k, v in headers.items():
                    log.debug(f'{k}: {v}')

                try:
                    if meth == 'GET' and not OFFLINE:
                        # direct streaming might be required...
                        preview = sess.head(uri, headers=headers,
                                            allow_redirects=False)
                        direct = None
                        if int(preview.headers.get('Content-Length', 0)) > BIG:
                            direct = f'file bigger than {BIG}'
                        if 'Range' in headers:
                            # There seems to be a bug in CacheControl
                            # that serves contents in full if a range request
                            # hits a non-ranged cached entry.
                            direct = f'ranged request, playing safe'
                        if direct:
                            # Don't cache, don't reencode, stream it as is
                            log.info(f'streaming {uri} directly ({direct})')
                            r = requests.get(uri, headers=headers, stream=True)
                            self._status_and_headers(r.status_code, r.headers)
                            self.copyfile(r.raw, self.wfile)
                            return

                    # fetch with caching
                    m_func = getattr(sess, meth.lower())
                    r = m_func(uri if '://' in uri else 'http://self' + uri,
                               headers=headers, allow_redirects=False)
                    data = r.content
                    length = int(r.headers.get('Content-Length', 0))
                    if len(data) != length:
                        data = hack_around_unpacking(uri, headers, data)
                    assert len(data) == length
                    self._status_and_headers(r.status_code, r.headers)
                except BrokenPipeError:
                    log.warning(f'Upwards broken pipe for {meth} {uri}')
                    time.sleep(2)  # to delay a re-request
                    return
                except ConnectionResetError:
                    log.warning(f'Upwards connection reset for {meth} {uri}')
                    time.sleep(2)  # to delay a re-request
                    return
                except requests.exceptions.ConnectionError:
                    log.warning(f'Upwards connection error for {meth} {uri}')
                    time.sleep(2)  # to delay a re-request
                    return
                log.debug(f'{meth} {basename} fetched {length} ({uri})')
                try:
                    if meth == 'GET':
                        self.wfile.write(data)
                except BrokenPipeError:
                    log.warning(f'Downwards broken pipe for {meth} {uri}')
                except ConnectionResetError:
                    log.warning(f'Downwards connection reset for {meth} {uri}')
                except requests.exceptions.ConnectionError:
                    log.warning(f'Downwards onnection error for {meth} {uri}')
                log.info(f'{meth} {basename} served {length} ({uri})')

            def do_HEAD(self):
                if self.path in http_cache._local_files_to_serve:
                    return super().do_HEAD()  # act as a HTTP server
                self._serve(uri=self.path, headers=self.headers, meth='HEAD')

            def do_GET(self):
                if self.path in http_cache._local_files_to_serve:
                    return super().do_GET()  # act as a HTTP server
                self._serve(uri=self.path, headers=self.headers, meth='GET')

            def log_message(self, format, *args):  # supress existing logging
                return

            def translate_path(self, http_path):  # directly serve local files
                local_path = http_cache._local_files_to_serve[http_path]
                log.info(f'serving {http_path} directly from {local_path}')
                return local_path

        httpd = ThreadingHTTPServer((host, port), Handler)
        _, self.port = httpd.socket.getsockname()
        threading.Thread(target=httpd.serve_forever, daemon=True).start()

    def _get_requests_session(self, direct=False):
        if not direct:
            cache = cachecontrol.caches.FileCache(path.downloads('cache'))
            sess = cachecontrol.CacheControl(requests.Session(), cache=cache)
        else:
            sess = requests.Session()
        for uri, kwargs in self._mocks:
            adapter = requests_mock.Adapter()
            adapter.register_uri('HEAD', uri, **kwargs)
            adapter.register_uri('GET', uri, **kwargs)
            sess.mount(uri, adapter)
        return sess

    def fetch(self, url, out_path):
        sess = self._get_requests_session()
        r = sess.get(url)
        with open(out_path, 'wb') as f:
            f.write(r.content)

    def mock(self, uri, text):
        """
        Mock a text file at some location.
        Examples:
          * mock('http://self/test', text='TEST')
            and access through proxy as `http://self/test`
        """
        content_length = {'Content-Length': str(len(text.encode()))}
        self._mocks.append((uri, {'text': text, 'headers': content_length}))

    def mock_custom(self, uri, **kwargs):
        """
        Mock a custom HTTP response.
        See ``help(requests_mock.Adapter.register_uri)`` for parameters.
        """
        self._mocks.append((uri, kwargs))

    def serve_local_file(self, http_path, local_path):
        """
        Serve this local file as an HTTP server.
        Examples:
          * serve('test', '/some/file')
            and access directly as `http://<host>:<port>/test`
          * serve('http://test', '/some/file')
            and access through proxy as `http://test`
        """
        self._local_files_to_serve[http_path] = local_path


# Hack around requests uncompressing Content-Encoding: gzip


def hack_around_unpacking(uri, headers, wrong_content):
    log.warning(f're-fetching correct content for {uri}')
    r = requests.get(uri, headers=headers, stream=True, allow_redirects=False)
    h = hashlib.sha256(wrong_content).hexdigest()
    cachefile = path.downloads('fixups', h, makedirs=True)
    if not os.path.exists(cachefile):
        with path.wip(cachefile) as wip:
            with open(wip, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    with open(cachefile, 'rb') as f:
        return f.read()


# Fully offline cache utilization functionality


def c_r_offline(self, request):
    cache_url = self.cache_url(request.url)
    log.debug(f'looking up {cache_url} in the cache')
    cache_data = self.cache.get(cache_url)
    if cache_data is None:
        log.error(f'{cache_url} not in cache and fingertip is offline')
        return False
    resp = self.serializer.loads(request, cache_data)
    if not resp:
        log.error(f'{cache_url} cache entry deserialization failed, ignored')
        return False
    log.warning(f'Using {cache_url} from offline cache')
    return resp


if OFFLINE:
    cachecontrol.controller.CacheController.cached_request = c_r_offline
