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

import re
import urllib.parse
from typing import Union, List

import yaml
import requests
import xnat
import taskclient

from flask import current_app
from studygovernor.models import ExternalSystem

from studygovernor.services.pidb import pidbservice


def do_callback(callback_url: str, state: str):
    data = {
        'state': state,
    }

    print('Callback to: {}, with data {}'.format(callback_url, data))
    response = requests.put(callback_url, json=data)
    print('RESPONSE [{}]: {}'.format(response.status_code, response.text))

    return "Callback to: {}, with data {}\nRESPONSE [{}]: {}".format(
        callback_url,
        data,
        response.status_code,
        response.text
    )


def update_url(url: str, **kwargs):
    if not isinstance(url, tuple):
        url = urllib.parse.urlparse(url)

    url = url._replace(**kwargs)
    return urllib.parse.urlunparse(url)


def download(url: str):
    # Find host to connect to
    split_url = urllib.parse.urlparse(url)
    host = urllib.parse.urlunparse(split_url._replace(path='', params='', query='', fragment=''))

    with xnat.connect(host, verify=False) as session:
        path = split_url.path

        resource, filename = path.split('/files/')
        print('Found desired filename: {}'.format(filename))
        if '{timestamp}' in path:
            pattern = filename.format(timestamp=r'(_?(?P<timestamp>\d\d\d\d\-\d\d\-\d\dT\d\d:\d\d:\d\d)_?)?') + '$'
        else:
            pattern = filename + '$'

        # Query all files and sort by timestamp
        files = session.get_json('{}/files'.format(resource))
        files = [x['Name'] for x in files['ResultSet']['Result']]
        print('Found file candidates {}, pattern is {}'.format(files, pattern))
        files = {re.match(pattern, x): x for x in files}
        files = {k.group('timestamp'): v for k, v in files.items() if k is not None}
        print('Found files: {}'.format(files))

        if len(files) == 0:
            return None

        # None is the first, timestamp come after that, so last one is highest timestamp
        latest_file = sorted(files.items())[-1][1]
        print('Select {} as being the latest file'.format(latest_file))

        # Construct the correct path again
        path = '{}/files/{}'.format(resource, latest_file)

        data = session.get_json(path)

    return data


def pidb(experiment_url: str,
         action_url: str,
         fields_uri: Union[str, List[str]],
         templates: Union[str, List[str]],
         done_state: str,
         failed_state: str,
         ifdb_external_system_name: str='PIDB',
         xnat_external_system_name: str='XNAT',
         taskmanager_external_system_name: str='TASKMANAGER'):
    """
    Add experiment to IFDB

    :param experiment_url: str,
    :param action_url: str,
    :param fields_uri: Union[str, List[str]],
    :param templates: Union[str, List[str]],
    :param done_state: str,
    :param failed_state: str,
    :param ifdb_external_system_name: str='IFDB',
    :param xnat_external_system_name: str='XNAT',
    :param taskmanager_external_system_name: str='TASKMANAGER'

    Example:

    .. code-block:: JSON

     {
        "function": "ifdb",
        "fields_uri": [
          "resources/FIELDS/files/mask_{timestamp}.json",
          "resources/FIELDS/files/QA_{timestamp}.json"
        ],
        "templates": [
          "mask",
          "manual_qa"
        ],
        "done_state": "/data/states/done",
        "failed_state": "/data/states/write_inspect_data_failed"
     }
    """
    # Get required information
    print('Experiment located at: {}'.format(experiment_url))
    experiment = requests.get(experiment_url).json()
    experiment_label = experiment['label']

    # Get subject information
    subject_url = experiment_url.replace(experiment['uri'], experiment['subject'])
    subject = requests.get(subject_url).json()
    subject_label = subject['label']

    # Get XNAT information
    xnat = ExternalSystem.query.filter(ExternalSystem.system_name == xnat_external_system_name).one()
    xnat_experiment_id = experiment['external_ids'][xnat_external_system_name]
    xnat_subject_id = subject['external_ids'][xnat_external_system_name]
    xnat_uri = xnat.url.rstrip('/')

    # Get IFDB information
    ifdb = ExternalSystem.query.filter(ExternalSystem.system_name == ifdb_external_system_name).one()
    ifdb_uri = ifdb.url.rstrip('/') + '/'

    # Get TaskManager information
    taskmanger = ExternalSystem.query.filter(ExternalSystem.system_name == taskmanager_external_system_name).one()
    taskmanager_uri = taskmanger.url.rstrip('/')

    # Create URI path for XNAT experiment
    xnat_experiment_path = "data/archive/projects/{project}/subjects/{subject}/experiments/{experiment}".format(
        project=current_app.config['STUDYGOV_XNAT_PROJECT'],
        subject=xnat_subject_id,
        experiment=xnat_experiment_id
    )

    if not isinstance(fields_uri, list):
        fields_uri = [fields_uri]

    if not isinstance(templates, list):
        templates = [templates]

    log_data = []

    for fields, task_template in zip(fields_uri, templates):
        # Find URI for fields file
        xnat_fields_uri = '{}/{}/{}'.format(xnat_uri, xnat_experiment_path, fields)
        json_data = download(xnat_fields_uri)

        taskman = taskclient.connect(taskmanager_uri)
        task_template_data = taskman.get(f'/task_templates/{task_template}').json()
        task_template_data = yaml.safe_load(task_template_data['content'])

        log_data.append("""
    IFDB server: {}
    Subject id: {}
    Subject url: {}
    Experiment scandate: {}
    Generator url: {}
    Template name: {}
    
    JSON data: {} 
    
    Template JSON data: {}
    """.format(ifdb_uri,
               subject_label,
               subject_url,
               experiment['scandate'],
               action_url,
               task_template,
               json_data,
               task_template_data))

        pidbservice.ingest_json(
            json_data,  # Fields file loaded and parsed
            task_template_data,  # Task template url/path/data?
            ifdb_uri,  # IFDB url
            task_template,  # Name of the task template
            subject_label,  # For RSS this is ergo_id
            subject_url,  # Subject uri in study governor
            experiment['scandate'],
            action_url
        )

    # Find callback url
    parsed_url = urllib.parse.urlparse(experiment_url)
    callback_url = update_url(parsed_url, path=parsed_url.path + '/state')
    result = True

    if result:
        print('SUCCESS')
        print('Calling callback with: {}'.format(done_state))
        log_data.append(do_callback(callback_url, done_state))
    else:
        print('FAILED')
        print('Calling callback with: {}'.format(failed_state))
        log_data.append(do_callback(callback_url, failed_state))

    log_data = '\n'.join(log_data)

    return log_data[:64000]

