# Copyright 2019 European Centre for Medium-Range Weather Forecasts (ECMWF)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

from __future__ import absolute_import, division, print_function, unicode_literals

import requests
import json
import time
import logging
import os
from tqdm import tqdm
from urllib.parse import urlparse
from ftplib import FTP


def bytes_to_string(n):
    u = ['', 'K', 'M', 'G', 'T', 'P']
    i = 0
    while n >= 1024:
        n /= 1024.0
        i += 1
    return '%g%s' % (int(n * 10 + 0.5) / 10.0, u[i])


def read_config(path):
    config = {}
    with open(path) as f:
        for l in f.readlines():
            if ':' in l:
                k, v = l.strip().split(':', 1)
                if k in ('url', 'user', 'password', 'token', 'verify'):
                    config[k] = v.strip()
    return config


def shorten(r, length=80):
    txt = json.dumps(r)
    if len(txt) > length:
        return txt[:length - 3] + "..."
    return txt


class FTPRequest:

    history = None
    is_redirect = False
    status_code = 200
    reason = ''
    headers = dict()
    raw = None

    def __init__(self, url, logger):

        self._logger = logger
        self._logger.warning("Downloading from FTP url: %s", url)

        parsed = urlparse(url)
        self._ftp = FTP(parsed.hostname)
        self._ftp.login(parsed.username, parsed.password)
        self._ftp.voidcmd('TYPE I')
        self._transfer, self._size = self._ftp.ntransfercmd("RETR %s" % (parsed.path, ))
        if self._size:
            self.headers['Content-Length'] = str(self._size)

    def raise_for_status(self):
        pass

    def close(self):
        self._ftp.close()

    def iter_content(self, chunk_size):

        while True:
            chunk = self._transfer.recv(chunk_size)
            if not chunk:
                break
            yield chunk


class FTPAdapter:

    def __init__(self, logger):
        self.logger = logger

    def send(self, request, *args, **kwargs):
        assert "Range" not in request.headers
        return FTPRequest(request.url, self.logger)


class RequestRunner:

    def __init__(self, client):
        self.get = client.get
        self.post = client.post
        self.debug = client.debug
        self.sleep_max = client.sleep_max

    def _run(self, query):
        result = self.post(query, self.action)
        jobId = result[self.idKey]

        status = result["status"]

        sleep = 1
        while status != "completed":
            assert status in ["started", "running"]
            self.debug("Sleeping %s seconds", sleep)
            time.sleep(sleep)
            result = self.get(self.action, 'status', jobId)
            status = result["status"]
            sleep *= 1.1
            if sleep > self.sleep_max:
                sleep = self.sleep_max

        return result, jobId


class DataRequestRunner(RequestRunner):

    action = 'datarequest'
    idKey = 'jobId'

    def _paginate(self, jobId):
        result = self.get(self.action, 'jobs', jobId, 'result')
        page = result
        for p in page["content"]:
            yield p

        while page.get("nextPage"):
            self.debug(json.dumps(page, indent=4))
            page = self.get(page["nextPage"])
            for p in page["content"]:
                yield p

    def run(self, query):
        _, jobId = self._run(query)
        return list(self._paginate(jobId)), jobId


class DataOrderRequest(RequestRunner):

    action = 'dataorder'
    idKey = 'orderId'

    def run(self, query):
        _, orderId = self._run(query)
        return ('dataorder', 'download', orderId)


class SearchResults:

    def __init__(self, client, results, jobId):
        self.client = client
        self.debug = client.debug
        self.stream = client.stream
        self.results = results
        self.jobId = jobId
        self.volume = sum(r.get('size', 0) for r in results)

    def __repr__(self):
        return "SearchResults[items=%s,volume=%s,jobId=%s]" % (len(self.results),
                                                               bytes_to_string(self.volume),
                                                               self.jobId,)

    def download(self):
        for result in self.results:
            query = {"jobId": self.jobId,
                     "uri": result['url']}
            self.debug(result)
            url = DataOrderRequest(self.client).run(query)
            self.stream(result.get('filename'), result.get('size'), *url)


class Client(object):

    logger = logging.getLogger('hda')

    def __init__(self,
                 url=os.environ.get('HDA_URL'),
                 user=os.environ.get('HDA_USER'),
                 password=os.environ.get('HDA_PASSWORD'),
                 token=os.environ.get('HDA_TOKEN'),
                 quiet=False,
                 debug=False,
                 verify=None,
                 timeout=None,
                 retry_max=500,
                 sleep_max=120,
                 info_callback=None,
                 warning_callback=None,
                 error_callback=None,
                 debug_callback=None,
                 progress=True,
                 ):

        if not quiet:

            if debug:
                level = logging.DEBUG
            else:
                level = logging.INFO

            logging.basicConfig(level=level,
                                format='%(asctime)s %(levelname)s %(message)s')

        dotrc = os.environ.get('HDA_RC', os.path.expanduser('~/.hdarc'))

        if url is None or (token is None and user is None and password is None):
            if os.path.exists(dotrc):
                config = read_config(dotrc)

                if token is None:
                    token = config.get('token')

                if user is None:
                    user = config.get('user')

                if password is None:
                    password = config.get('password')

                if url is None:
                    url = config.get('url')

                if verify is None:
                    verify = int(config.get('verify', 1))

        if url is None or (token is None and user is None):
            raise Exception('Missing/incomplete configuration file: %s' % (dotrc))

        self.url = url
        self.token = token
        self.user = user
        self.password = password

        self.quiet = quiet
        self.verify = True if verify else False
        self.timeout = timeout
        self.sleep_max = sleep_max
        self.retry_max = retry_max
        self.progress = progress

        self.debug_callback = debug_callback
        self.warning_callback = warning_callback
        self.info_callback = info_callback
        self.error_callback = error_callback

        self._session = None

        self.debug("HDA %s", dict(url=self.url,
                                  token=self.token,
                                  user=self.user,
                                  password=self.password,
                                  quiet=self.quiet,
                                  verify=self.verify,
                                  timeout=self.timeout,
                                  sleep_max=self.sleep_max,
                                  retry_max=self.retry_max,
                                  progress=self.progress,
                                  ))

    def full_url(self, *args):

        if len(args) == 1 and args[0].split(':')[0] in ('http', 'https'):
            return args[0]

        full = "/".join([str(x) for x in [self.url] + list(args)])
        return full

    @property
    def session(self):
        if self._session is None:
            session = requests.Session()
            if self.token is None:
                session.auth = (self.user, self.password)
                full = self.full_url('gettoken')
                self.debug("===> GET %s", full)
                r = self.robust(session.get)(full)
                r.raise_for_status()
                result = r.json()
                self.debug("<=== %s", shorten(result))
                self.token = result['access_token']
                session.auth = None
            session.headers = {"Authorization": self.token}
            session.mount("ftp://", FTPAdapter(self))
            self._session = session
            self.debug("Token is %s", self.token)

        return self._session

    def info(self, *args, **kwargs):
        if self.info_callback:
            self.info_callback(*args, **kwargs)
        else:
            self.logger.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        if self.warning_callback:
            self.warning_callback(*args, **kwargs)
        else:
            self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self.error_callback:
            self.error_callback(*args, **kwargs)
        else:
            self.logger.error(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.debug_callback:
            self.debug_callback(*args, **kwargs)
        else:
            self.logger.debug(*args, **kwargs)

    def robust(self, call):

        def retriable(code, reason):

            if code in [requests.codes.internal_server_error,
                        requests.codes.bad_gateway,
                        requests.codes.service_unavailable,
                        requests.codes.gateway_timeout,
                        requests.codes.too_many_requests,
                        requests.codes.request_timeout]:
                return True

            return False

        def wrapped(*args, **kwargs):
            tries = 0
            while tries < self.retry_max:
                try:
                    r = call(*args, **kwargs)
                except requests.exceptions.ConnectionError as e:
                    r = None
                    self.warning("Recovering from connection error [%s], attemx ps %s of %s",
                                 e, tries, self.retry_max)

                if r is not None:
                    if not retriable(r.status_code, r.reason):
                        return r
                    self.warning("Recovering from HTTP error [%s %s], attemps %s of %s",
                                 r.status_code, r.reason, tries, self.retry_max)

                tries += 1

                self.warning("Retrying in %s seconds", self.sleep_max)
                time.sleep(self.sleep_max)

        return wrapped

    def search(self, query):
        return SearchResults(self, *DataRequestRunner(self).run(query))

    def _datasets(self):
        page = self.get('datasets')
        for p in page["content"]:
            yield p

        while page.get("nextPage"):
            page = self.get(page["nextPage"])
            for p in page["content"]:
                yield p

    def datasets(self):
        return list(self._datasets())

    def dataset(self, datasetId):
        return self.get('datasets', datasetId)

    def metadata(self, datasetId):
        return self.get('querymetadata', datasetId)

    def get(self, *args):

        if self.debug:
            self.session  # Force login
        full = self.full_url(*args)
        self.debug("===> GET %s", full)
        r = self.robust(self.session.get)(full, timeout=self.timeout)
        r.raise_for_status()
        result = r.json()
        self.debug("<=== %s", shorten(result))
        return result

    def post(self, message, *args):

        if self.debug:
            self.session  # Force login

        full = self.full_url(*args)
        self.debug("===> POST %s", full)
        self.debug("===> POST %s", shorten(message))

        r = self.robust(self.session.post)(full, json=message, timeout=self.timeout)
        r.raise_for_status()
        result = r.json()
        self.debug("<=== %s", shorten(result))
        return result

    def stream(self, target, size, *args):
        full = self.full_url(*args)

        self.info("Downloading %s to %s (%s)", full, target, bytes_to_string(size))
        start = time.time()

        mode = 'wb'
        total = 0
        sleep = 10
        tries = 0
        headers = None

        while tries < self.retry_max:

            r = self.robust(self.session.get)(full,
                                              stream=True,
                                              verify=self.verify,
                                              headers=headers,
                                              timeout=self.timeout)
            try:
                r.raise_for_status()

                self.debug("Headers: %s", r.headers)

                with tqdm(total=size,
                          unit_scale=True,
                          unit_divisor=1024,
                          unit='B',
                          disable=not self.progress,
                          leave=False,
                          ) as pbar:
                    pbar.update(total)
                    with open(target, mode) as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                total += len(chunk)
                                pbar.update(len(chunk))

            except requests.exceptions.ConnectionError as e:
                self.error("Download interupted: %s" % (e,))
            finally:
                r.close()

            if total >= size:
                break

            self.error("Download incomplete, downloaded %s byte(s) out of %s" % (total, size))

            if isinstance(r, FTPAdapter):
                self.warning("Ignoring size mismatch")
                return target

            self.warning("Sleeping %s seconds" % (sleep,))
            time.sleep(sleep)
            mode = 'ab'
            total = os.path.getsize(target)
            sleep *= 1.5
            if sleep > self.sleep_max:
                sleep = self.sleep_max
            headers = {'Range': 'bytes=%d-' % total}
            tries += 1
            self.warning("Resuming download at byte %s" % (total, ))

        if total < size:
            raise Exception("Download failed: downloaded %s byte(s) out of %s (missing %s)" % (total, size, size - total))

        if total > size:
            self.warning("Oops, downloaded %s byte(s), was supposed to be %s (extra %s)" % (total, size, total - size))

        elapsed = time.time() - start
        if elapsed:
            self.info("Download rate %s/s", bytes_to_string(size / elapsed))

        return target
