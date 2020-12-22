import json
import logging
import os
from typing import Any, Dict, Optional, Union
import zipfile

import requests

logger = logging.getLogger(__name__)


class Client:

    def __init__(self, host, port=None, protocol='https', authenticator: Union[Any, str] = None, headers: Optional[Dict[str, str]] = None):
        self.host = host
        self.port = port
        self.protocol = protocol
        if headers is None:
            headers = {}
        self._headers = headers
        if hasattr(authenticator, 'session'):
            self._headers.update(authenticator.session.headers)
        elif isinstance(authenticator, str):
            # Assume this is a token
            self._headers = self._with_auth_headers(self._headers, authenticator)
        self.__upload_token = None
        self._auth_session = None
        self._upload_session = None

    @staticmethod
    def _with_auth_headers(headers=None, token=None):
        if headers is None:
            headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers

    def _make_session(self, headers=None, token=None):
        session = requests.sessions.Session()

        if headers is None:
            headers = {}
        headers = self._with_auth_headers(headers.copy(), token)
        session.headers.update(headers)
        return session

    @property
    def session(self):
        """Get a requests session with authentication if provided."""
        if self._auth_session is None:
            self._auth_session = self._make_session(self._headers)
        return self._auth_session

    @property
    def upload_session(self):
        """Get a requests session with authentication if provided."""
        if self._upload_session is None:
            if self.__upload_token is None:
                self.get_upload_token()
            self._upload_session = self._make_session(self._headers.copy(), self.__upload_token)
        return self._upload_session

    @property
    def base_url(self):
        if self.port:
            return f'{self.protocol}://{self.host}:{self.port}'
        else:
            return f'{self.protocol}://{self.host}'

    def get_upload_token(self):
        r = self.session.get(f'{self.base_url}/api/auth/token/upload')
        r.raise_for_status()
        self.__upload_token = r.json()['access_token']

    @staticmethod
    def create_zipfile(html_path, working_dir=None):
        if working_dir is None:
            working_dir = os.getcwd()
        logger.debug(f'Creating zipfile in: {working_dir}')
        zip_fname = os.path.join(working_dir, 'docs-upload.zip')
        zipf = zipfile.ZipFile(zip_fname, 'w', zipfile.ZIP_DEFLATED)
        for dirname, _, files in os.walk(html_path):
            for filename in files:
                filepath = os.path.join(dirname, filename)
                zipf.write(filepath, arcname=os.path.relpath(filepath, html_path))
        zipf.close()
        logger.debug(f'Created zipfile: {zip_fname}')
        return zip_fname

    def upload_zipfile(self, zipfile, name, version, repository, tags=None, ):
        if tags is None:
            tags = list()
        logger.debug(f'Uploading zipfile: {zipfile}')
        values = json.dumps({'version': version,
                             'name': name,
                             'repository': repository,
                             'tags': tags})
        logger.debug(f'Using values: {values}')
        response = self.upload_session.post(f'{self.base_url}/api/docs/upload', data=values)

        logger.debug(f'Request: {response.request.method} {response.request.url} {response.request.headers} {response.request.body[:1000]}')
        logger.debug(f'Result: {response.content}')
        response.raise_for_status()
        upload_url = response.content.decode().split('Location: ')[1][:-1].replace('http://', f'{self.protocol}://').replace('https://', f'{self.protocol}://')
        logger.debug(f'Uploading package to: {upload_url}')
        response = self.upload_session.put(upload_url, files={'documentation': ('docs-upload.zip', open(zipfile, 'rb').read())})

        logger.debug(f'Request: {response.request.method} {response.request.url} {response.request.headers} {response.request.body[:1000]}')
        logger.debug(f'Result: {response.content}')
        response.raise_for_status()
        logger.info(f'Upload Complete')
        return response

    def upload_dir(self, html_path, name, version, repository, tags=None, working_dir=None):
        self.upload_zipfile(self.create_zipfile(html_path, working_dir), name, version, repository, tags)
