# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
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

import requests

from six.moves.urllib import parse

from . import exceptions
from . import models
from .util.helpers import get_object_from_arg


class StudyGovernorSession(object):
    def __init__(self, server, debug=True):
        self._server = parse.urlparse(server)
        self._interface = requests.Session()
        self.debug = debug

    @property
    def interface(self):
        """
        The underlying `requests <https://requests.readthedocs.org>`_ interface used.
        """
        return self._interface

    def _check_response(self, response, accepted_status=None, uri=None):
        if self.debug:
            print('[DEBUG] Received response with status code: {}'.format(response.status_code))

        if accepted_status is None:
            accepted_status = [200, 201, 202, 203, 204, 205, 206]  # All successful responses of HTML
        if response.status_code not in accepted_status or response.text.startswith(('<!DOCTYPE', '<html>')):
            raise exceptions.RESTResponseError('Invalid response from the StudyGovernorSession for url {} (status {}):\n{}'.format(uri, response.status_code, response.text))

    def get(self, path, params=None, format=None, query=None, accepted_status=None):
        accepted_status = accepted_status or [200]
        uri = self._format_uri(path, format, query=query)

        if self.debug:
            print('[DEBUG] GET URI {}'.format(uri))

        try:
            response = self.interface.get(uri, params=params)
        except requests.exceptions.SSLError:
            raise exceptions.StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow OK, as we want to get data
        return response

    def post(self, path, data=None, format=None, query=None, accepted_status=None, json=None):
        accepted_status = accepted_status or [200, 201]
        uri = self._format_uri(path, format, query=query)

        if self.debug:
            print('[DEBUG] POST URI {}'.format(uri))
            print('[DEBUG] POST JSON {}'.format(json))

        try:
            response = self._interface.post(uri, data=data, json=json)
        except requests.exceptions.SSLError:
            raise exceptions.StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def put(self, path, data=None, files=None, format=None, query=None, accepted_status=None, json=None):
        accepted_status = accepted_status or [200, 201]
        uri = self._format_uri(path, format, query=query)

        if self.debug:
            print('[DEBUG] PUT URI {}'.format(uri))
            print('[DEBUG] PUT JSON {}'.format(json))

        try:
            response = self._interface.put(uri, data=data, files=files, json=json)
        except requests.exceptions.SSLError:
            raise exceptions.StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow created OK or Create status (OK if already exists)
        return response

    def delete(self, path, headers=None, accepted_status=None, query=None):
        accepted_status = accepted_status or [200]
        uri = self._format_uri(path, query=query)

        if self.debug:
            print('[DEBUG] DELETE URI {}'.format(uri))
            print('[DEBUG] DELETE HEADERS {}'.format(headers))

        try:
            response = self.interface.delete(uri, headers=headers)
        except requests.exceptions.SSLError:
            raise exceptions.StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def _format_uri(self, path, format=None, query=None):
        if path[0] != '/':
            raise ValueError('The requested URI path should start with a / (e.g. /api/v1/projects), found {}'.format(path))

        if query is None:
            query = {}

        if format is not None:
            query['format'] = format

        # Create the query string
        if len(query) > 0:
            query_string = parse.urlencode(query)
        else:
            query_string = ''

        data = (self._server.scheme,
                self._server.netloc,
                self._server.path.rstrip('/') + path,
                '',
                query_string,
                '')

        return parse.urlunparse(data)

    def get_json(self, uri, query=None):
        response = self.get(uri, format='json', query=query)
        try:
            return response.json()
        except ValueError:
            raise ValueError('Could not decode JSON from {}'.format(response.text))

    def set_state(self, experiment, state, freetext=None):
        """
        Transition the experiment to a state.

        :param experiment: Experiment URI
        :param state: Name of the state to transition to.
        """

        try:
            response = self.put(
                    '{}/state'.format(experiment),
                    json={
                        "state": state,
                        "freetext": freetext
                        }
                    )
        except requests.RequestException as e:
            print("Something went wrong while communicating with the server. ({})".format(e))
            response = None
        return response
