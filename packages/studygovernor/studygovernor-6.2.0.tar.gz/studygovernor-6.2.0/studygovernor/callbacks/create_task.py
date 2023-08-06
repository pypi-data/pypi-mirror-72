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

import json
import netrc
import os
from string import Template
from urllib.parse import urlparse

import requests
from flask import current_app

import logging


def create_task(experiment_url: str,
                action_url: str,
                task_base,
                task_info,
                progress_state=None,
                done_state=None,
                xnat_external_system: str='XNAT',
                taskmanager_external_system_name: str='TASKMANAGER'):
    """
    Create taskmanager task

    :param experiment_url: experiment url
    :param action_url: action url
    :param task_base: task_base is a Template that contains info for the task
    :param task_info: Additional info for the task as a list of [key1 val1 key2 val2 ...]
    :param progress_state: State while queued 
    :param done_state: State when done 
    :param xnat_external_system_name: name of the external xnat [XNAT]
    :param taskmanager_external_system_name: Taskmanager external ID

    Example:

    .. code-block:: JSON

       {
         "function": "create_task",
         "task_base": "manual_qa.json",
         "task_info": {
             "project": "sandbox",
             "application_name": "ViewR",
             "application_version": "5.1.4",
             "template": "manual_qa",
             "tags": ["QA", "Quality Assurance"],
             "distribute_in_group": "quality_assurance"
         },
         "done_state": "/api/v1/states/Automated_processing",
         "progress_state": "/api/v1/states/Queued_for_manual_qa"
       }

    """
    # Get External system urls
    logging.debug(f"Starting callback for action_url: {action_url}")
    external_system_endpoint_xnat = urlparse(action_url)._replace(
        path=f'/api/v1/external_systems/{xnat_external_system}'
    )
    external_system_endpoint_taskmanager = urlparse(action_url)._replace(
        path=f'/api/v1/external_systems/{taskmanager_external_system_name}'
    )

    xnat_response = requests.get(external_system_endpoint_xnat.geturl())
    taskmanager_response = requests.get(external_system_endpoint_taskmanager.geturl())

    task_manager_server = taskmanager_response.json()['url'].rstrip('/')
    xnat_server = xnat_response.json()['url'].rstrip('/')
    logging.debug(f"Using xnat: {xnat_server}")
    logging.debug(f"Using taskmanager: {task_manager_server}")

    # Get required information
    print('Experiment located at: {}'.format(experiment_url))
    experiment = requests.get(experiment_url).json()
    xnat_experiment_id = experiment['external_ids'][xnat_external_system]
    subject_url = experiment_url.replace(experiment['uri'], experiment['subject'])
    subject = requests.get(subject_url).json()
    xnat_subject_id = subject['external_ids'][xnat_external_system]

    label = experiment['label']

    # Check for additional information in the action
    response = requests.get(action_url)
    try:
        action_data = response.json()
    except ValueError:
        # No worries
        action_data = None

    # Read action freetext to find extra tags
    if isinstance(action_data, dict) and 'freetext' in action_data:
        try:
            extra_tags = json.loads(action_data['freetext'])
        except (TypeError, ValueError):
            extra_tags = None

    # Inject extra tags in task_info
    if extra_tags:
        if 'tags' in task_info:
            task_info['tags'].extend(extra_tags)
        else:
            task_info['tags'] = extra_tags
    
    # Inject the generator_url (= action_url) in the task_info
    task_info['generator_url'] = action_url

    # Get task base from the correct directory
    # task_bases = os.listdir(current_app.config['STUDYGOV_PROJECT_TASKS'])
    task_bases = os.listdir(current_app.config['STUDYGOV_PROJECT_TASKS'])

    if task_base in task_bases:
        task_base_file = os.path.join(current_app.config['STUDYGOV_PROJECT_TASKS'], task_base)

        # Check if task base file is valid
        if not (isinstance(task_base_file, str) and os.path.isfile(task_base_file)):
            raise ValueError('Task base is in "{}" is not valid'.format(task_base_file))
    else:
        raise ValueError('Task base "{}" not found!'.format(task_base))

    # Read the file and fill out the base
    print('Loading taskbase file {}'.format(task_base_file))
    with open(task_base_file) as input_file:
        task_base = input_file.read()

    task_content = Template(task_base).substitute(EXPERIMENT_ID=xnat_experiment_id,
                                                  SUBJECT_ID=xnat_subject_id,
                                                  LABEL=label,
                                                  SYSTEM_URL=xnat_server)

    # Update fields with per-experiment information
    task_info['content'] = task_content
    task_info['callback_url'] = "{experiment}/state".format(experiment=experiment_url)
    if done_state is not None:
        task_info['callback_content'] = json.dumps({"state": done_state})
    else:
        task_info['callback_content'] = json.dumps({})

    url = '{url}/api/v1/tasks'.format(url=task_manager_server)

    # Check if there is login information in netrc
    netloc = urlparse(url).netloc
    try:
        auth_info = netrc.netrc().authenticators(netloc)
    except IOError:
        auth_info = None

    print('Found auth_info for {}: {}'.format(netloc, auth_info is not None))

    # Send the task to the taskmanager
    if auth_info is None:
        response = requests.post(url, json=task_info)
    else:
        response = requests.post(url, json=task_info, auth=(auth_info[0], auth_info[2]))

    if response.status_code not in [200, 201]:
        raise ValueError('Response had invalid status: [{}]: {}'.format(response.status_code, response.text))

    task_query_result = \
"""Created task
url: {}
payload: {}
status code: {}
response text: {}""".format(url, task_info, response.status_code, response.text)

    # Set the progress state
    if progress_state is not None:
        url = '{experiment}/state'.format(experiment=experiment_url)
        payload = {"state": progress_state}
        response = requests.put(url, json=payload)

        if response.status_code not in [200]:
            raise ValueError('Response had invalid status: [{}]: {}'.format(response.status_code, response.text))

        progress_query_result = \
"""Updated state:
url: {}
payload: {}
status code: {}
response text: {}""".format(url, payload, response.status_code, response.text)
    else:
        progress_query_result = ""

    # Truncate the result if needed
    progress_query_result = progress_query_result[-16000:]
    task_query_len = 64000 - len(progress_query_result)
    task_query_result = task_query_result[-task_query_len:]

    logging.debug(f"Finished callback for url: {action_url}")

    return "{}\n{}".format(task_query_result, progress_query_result)
