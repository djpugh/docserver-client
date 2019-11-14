import json
import logging
import os
import zipfile

import requests


logger = logging.getLogger(__name__)


class Client:

    def __init__(self, host, port=None, protocol='https', token=None):
        self.host = host
        self.port = port
        self.token = token
        self.protocol = protocol

    @property
    def base_url(self):
        if self.port:
            return f'{self.protocol}://{self.host}:{self.port}'
        else:
            return f'{self.protocol}://{self.host}'

    def get_upload_token(self, api_token):
        r = requests.get(f'{self.base_url}/api/auth/token/upload', headers={'Authorization': f'Bearer {api_token}'})
        r.raise_for_status()
        self.token = r.json()['access_token']

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
        response = requests.post(f'{self.base_url}/api/docs/upload', data=values,
                                 headers={'Authorization': f'Bearer {self.token}'})

        logger.debug(f'Request: {response.request.method} {response.request.url} {response.request.headers} {response.request.body[:100]}')
        logger.debug(f'Result: {response.content}')
        response.raise_for_status()
        upload_url = response.content.decode().split('Location: ')[1][:-1].replace('http://', f'{self.protocol}://').replace('https://', f'{self.protocol}://')
        logger.debug(f'Uploading package to: {upload_url}')
        response = requests.put(upload_url, files={'documentation': ('docs-upload.zip', open(zipfile, 'rb').read())},
                                headers={'Authorization': f'Bearer {self.token}'})

        logger.debug(f'Request: {response.request.method} {response.request.url} {response.request.headers} {response.request.body[:1000]}')
        logger.debug(f'Result: {response.content}')
        response.raise_for_status()
        logger.info(f'Upload Complete')
        return response

    def upload_dir(self, html_path, name, version, repository, tags=None, working_dir=None):
        self.upload_zipfile(self.create_zipfile(html_path, working_dir), name, version, repository, tags)
