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

"""
Run a fastr network as the callback, the definition of the callback should
be like the following example:

    "callback": {
      "function": "fastr",
      "network_id": "cvon_prep",
      "source_mapping": {
        "t1": "/scans/s T1W_3D_TFE*/resources/DICOM",
        "flair": "/scans/3D_Brain*FLAIR*/resources/DICOM",
        "swi":  "/scans/SWI EPI 2min*/resources/DICOM",
        "asl": "/scans/ASL SENSE/resources/DICOM",
        "m0": "/scans/M0 meting SENSE/resources/DICOM"
      },
      "sink_mapping": {
        "t1_nii": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/image{ext}",
        "flair_nii": "/scans/3D_Brain*FLAIR*/resources/NIFTI/files/image{ext}",
        "swi_nii": "/scans/SWI EPI 2min*/resources/NIFTI/files/image{ext}",
        "asl_nii": "/scans/ASL SENSE/resources/NIFTI/files/image{ext}",
        "m0_nii": "/scans/M0 meting SENSE/resources/NIFTI/files/image{ext}",
        "flair_coregistered": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/flair_coreg_to_t1{ext}",
        "swi_coregistered": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/swi_coreg_to_t1{ext}",
        "asl_header_json": "/scans/ASL SENSE/resources/JSON/files/dicom_header{ext}",
        "m0_header_json": "/scans/M0 meting SENSE/resources/JSON/files/dicom_header{ext}"
      },
      "log_dir": "/home/cvon/.prep_logs/",
      "process_state": "preprocessing",
      "done_state": "preprocessing_finished",
      "failed_state": "preprocessing_failed",
      "fastr_home": "~/.fastr_testing"
    },
"""

import os
import re
import json
import pprint
import shutil
import signal
import subprocess
from urllib.parse import urlparse, urlunparse, urlencode

from typing import Mapping, Optional

import requests
import logging

from flask import current_app
from studygovernor.models import ExternalSystem


def create_uri(xnat_uri: str, extra_path:str, extra_query: Mapping[str, str]=None):
    if extra_query is None:
        query = {}
    else:
        query = dict(extra_query)

    parsed_url = urlparse(xnat_uri)
    if parsed_url.scheme == 'http':
        query['insecure'] = 'true'
        path = parsed_url.path
    elif parsed_url.scheme == 'https':
        query['insecure'] = 'false'
        path = parsed_url.path
    else:
        raise ValueError('XNAT uri should be http or https, found {}'.format(parsed_url.scheme))

    path = '{}/{}'.format(path.rstrip('/'), extra_path.lstrip('/'))

    if '{latest_timestamp}' in path:
        resource, filename = path.split('/files/', 1)
        pattern = filename.format(latest_timestamp=r'(_?(?P<timestamp>\d\d\d\d\-\d\d\-\d\dT\d\d:\d\d:\d\d(\.\d+)?)_?)?') + '$'

        # Query all files and sort by timestamp
        files = requests.get('{}/{}/files'.format(xnat_uri.rstrip('/'), resource.lstrip('/'))).json()
        files = [x['Name'] for x in files['ResultSet']['Result']]
        print('Found file candidates {}, pattern is {}'.format(files, pattern))
        files = {re.match(pattern, x): x for x in files}
        files = {k.group('timestamp'): v for k, v in files.items() if k is not None}
        print('Found files: {}'.format(files))

        if len(files) >= 1:
            # None is the first, timestamp come after that, so last one is highest timestamp
            latest_file = sorted(files.items())[-1][1]
            print('Select {} as being the latest file'.format(latest_file))

            # Construct the correct path again
            path = '{}/files/{}'.format(resource, latest_file)


    # Convert query dict to str
    qs = urlencode(query)
    url_parts = (
        'xnat',  # Scheme
        parsed_url.netloc,  # Netloc
        path,  # Path
        '',  # Params
        qs,  # Query
        ''  # Fragment
    )

    return urlunparse(url_parts)


def create_source_sink_data(xnat_uri: str,
                            project: str,
                            experiment: str,
                            source_mapping: Mapping[str, str],
                            sink_mapping: Mapping[str, str],
                            subject=None,
                            label=None):
    if subject is None:
        subject = '*'

    if label is None:
        label = experiment

    experiment_path = "data/archive/projects/{project}/subjects/{subject}/experiments/{experiment}".format(project=project,
                                                                                                           subject=subject,
                                                                                                           experiment=experiment)

    # Example source mapping
    # source_mapping = {
    #    "t1": "/scans/s T1W_3D_TFE*/resources/DICOM",
    #    "flair": "/scans/3D_Brain*FLAIR*/resources/DICOM",
    #    "swi":  "/scans/SWI EPI 2min*/resources/DICOM",
    #    "asl": "/scans/ASL SENSE/resources/DICOM",
    #    "m0": "/scans/M0 meting SENSE/resources/DICOM",
    # }

    # Example sink mapping
    # sink_data = {
    #    "t1_nii": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/image{ext}",
    #    "flair_nii": "/scans/3D_Brain*FLAIR*/resources/NIFTI/files/image{ext}",
    #    "swi_nii": "/scans/SWI EPI 2min*/resources/NIFTI/files/image{ext}",
    #    "asl_nii": "/scans/ASL SENSE/resources/NIFTI/files/image{ext}",
    #    "m0_nii": "/scans/M0 meting SENSE/resources/NIFTI/files/image{ext}",
    #    "flair_coregistered": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/flair_coreg_to_t1{ext}",
    #    "swi_coregistered": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/swi_coreg_to_t1{ext}",
    #    "asl_header_json": "/scans/ASL SENSE/resources/JSON/files/dicom_header{ext}",
    #    "m0_header_json": "/scans/M0 meting SENSE/resources/JSON/files/dicom_header{ext}",
    # }


    # Wrap the paths into a full-fledged uri
    source_mapping = {k: {label: create_uri(xnat_uri, experiment_path + v)} for k, v in source_mapping.items()}
    sink_query = {'resource_type': 'xnat:resourceCatalog',
                  'assessors_type': 'xnat:qcAssessmentData'}
    sink_mapping = {k: create_uri(xnat_uri, experiment_path + v, sink_query) for k, v in sink_mapping.items()}

    return source_mapping, sink_mapping


def do_callback(callback_url: str, state: str):
    data = {
        'state': state,
    }

    print('Callback to: {}, with data {}'.format(callback_url, data))
    response = requests.put(callback_url, json=data)

    print('RESPONSE [{}]: {}'.format(response.status_code, response.text))


def update_url(url: str, **kwargs):
    if not isinstance(url, tuple):
        url = urlparse(url)

    url = url._replace(**kwargs)
    return urlunparse(url)


def run_network(network_id: str, source_data: Mapping, sink_data: Mapping[str, str], label: str, fastr_home: Optional[str]):
    print('SOURCE: {}'.format(source_data))
    print('SINK: {}'.format(sink_data))
    network_files = os.listdir(current_app.config['STUDYGOV_PROJECT_NETWORKS'])

    tmpdir = os.path.join(current_app.config['STUDYGOV_PROJECT_SCRATCH'], 'fastr_{}_{}'.format(network_id, label))
    code_file_path = tmpdir + '.py'
    stdout_path = tmpdir + '_stdout.txt'
    stderr_path = tmpdir + '_stderr.txt'
    # Create a networkfile that can be run commandline in a fastr/python module environment
    with open(code_file_path, 'w') as code_file:
        code_file.write(
"""#!/bin/env python
# Autogenerated file for network execution via module

import imp
import fastr

# Log to console and reinitialize to take redirected stdout
fastr.config.logtype = 'console'
fastr.config._update_logging()

source_data = {source_data}

sink_data = {sink_data}

""".format(source_data=json.dumps(source_data, indent=4),
           sink_data=json.dumps(sink_data, indent=4))
        )

        if '{}.json'.format(network_id) in network_files:
            network_file = os.path.join(current_app.config['STUDYGOV_PROJECT_NETWORKS'], '{}.json'.format(network_id))
            network_file_path = tmpdir + '_network.json'
            shutil.copy2(network_file, network_file_path)
            code_file.write("network = fastr.Network.loadf('{}')\n".format(network_file_path))
        elif '{}.py'.format(network_id) in network_files:
            network_file = os.path.join(current_app.config['STUDYGOV_PROJECT_NETWORKS'], '{}.py'.format(network_id))
            network_file_path = tmpdir + '_network.py'
            shutil.copy2(network_file, network_file_path)
            code_file.write("network_module = imp.load_source('{}', '{}')\n".format(network_id, network_file_path))
            code_file.write("network = network_module.create_network()\n")
        else:
            raise ValueError('Could not find network file for {}'.format(network_id))

        print('TMPDIR: {}'.format(tmpdir))
        code_file.write("run = network.execute(source_data, sink_data, tmpdir='vfs://tmp/fastr_{}_{}')\n".format(network_id, label))
        code_file.write("exit(0 if run.result else 1)\n")

    if os.path.exists(tmpdir):
        print('Removing old tmpdir: {}'.format(tmpdir))
        if os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir)
        else:
            os.remove(tmpdir)

    log_data = \
"""Running network {}
code file: {}
scratch dir: {}
stdout log: {}
stderr log: {}
fastr home: {}

source data
-----------
{}

sink data
---------
{}

""".format(network_id,
           code_file_path,
           tmpdir,
           stdout_path,
           stderr_path,
           fastr_home,
           pprint.pformat(source_data, indent=2, width=60),
           pprint.pformat(sink_data, indent=2, width=60))

    # Write the progress to own files
    with open(stdout_path, 'w') as stdout, open(stderr_path, 'w') as stderr:
        if fastr_home:
            os.environ['FASTRHOME'] = fastr_home
        process = subprocess.Popen(['fastr_python_launcher', code_file_path], stdout=stdout, stderr=stderr)
        return_value = process.wait()

    if return_value == 0 and os.path.exists(tmpdir):
        print('Removing tmpdir after success: {}'.format(tmpdir))
        if os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir)
        else:
            os.remove(tmpdir)

    return return_value == 0, log_data


def fastr(experiment_uri: str,
          action_uri: str,
          network_id: str,
          source_mapping: Mapping[str, str],
          sink_mapping: Mapping[str, str],
          log_dir: str,
          process_state: str,
          done_state: str,
          failed_state: str,
          xnat_external_system_name: str='XNAT',
          fastr_home: Optional[str]=None):
    """
    Execute Fastr pipeline

    :param experiment_uri: experiment uri
    :param action_uri: action uri
    :param network_id: network that gets executed
    :param source_mapping: Mapping[str, str],
    :param sink_mapping: Mapping[str, str],
    :param log_dir: str,
    :param process_state: str,
    :param done_state: str,
    :param failed_state: str,
    :param xnat_external_system_name: name of the external xnat [XNAT]
    :param fastr_home: optionally, set the FASTRHOME variable passed to fastr

    Example:

    .. code-block:: JSON

       {
         "function": "fastr",
         "network_id": "preprocessing",
         "source_mapping": {
           "t1": "/scans/T1W*/resources/DICOM",
           "flair": "/scans/*FLAIR*/resources/DICOM",
         },
         "sink_mapping": {
           "t1_nii": "/scans/T1W*/resources/NIFTI/files/image{ext}",
           "flair_nii": "/scans/*FLAIR*/resources/NIFTI/files/image{ext}",
           "flair_coregistered": "/scans/T1W*/resources/NIFTI/files/flair_to_t1{ext}",
         },
         "log_dir": "/home/logs/",
         "process_state": "preprocessing",
         "done_state": "preprocessing_finished",
         "failed_state": "preprocessing_failed"
       }

    """
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    # Get XNAT address from database
    logging.debug(f"Starting callback for action_uri: {action_uri}")
    external_system_endpoint_xnat = urlparse(action_uri)._replace(path='/api/v1/external_systems/XNAT')
    xnat_response = requests.get(external_system_endpoint_xnat.geturl())  
    xnat_server = xnat_response.json()['url'].rstrip('/')
    logging.debug(f"Using xnat: {xnat_server}")
    
    parsed_url = urlparse(experiment_uri)
    experiment_id = parsed_url.path.split('/')[-1]
    
    # Find callback url
    callback_url = update_url(parsed_url, path=parsed_url.path + '/state')
    process_state = process_state

    print('Calling callback with: {}'.format(process_state))
    do_callback(callback_url, process_state)

    # Fetch data
    print('Get all required information from study manager')
    experiment = requests.get(experiment_uri).json()
    xnat_experiment_id = experiment['external_ids']['XNAT']
    experiment_label = experiment['label']

    subject_url = update_url(parsed_url, path=experiment['subject'])
    subject = requests.get(subject_url).json()
    xnat_subject_id = subject['external_ids']['XNAT']

    # Create source and sink data
    try:
        source_data, sink_data = create_source_sink_data(xnat_uri=xnat_server,
                                                         project=current_app.config['STUDYGOV_XNAT_PROJECT'],
                                                         experiment=xnat_experiment_id,
                                                         source_mapping=source_mapping,
                                                         sink_mapping=sink_mapping,
                                                         subject=xnat_subject_id,
                                                         label=experiment_label)

        result, log_data = run_network(network_id, source_data, sink_data, experiment_id, fastr_home)
    except Exception as excp:
        # If something goes wrong, transitino to failed state
        do_callback(callback_url, failed_state)
        raise

    print('RESULT STATES: S {} / F {}'.format(done_state, failed_state))

    if result:
        print('SUCCESS')
        print('Calling callback with: {}'.format(done_state))
        do_callback(callback_url, done_state)
    else:
        print('FAILED')
        print('Calling callback with: {}'.format(failed_state))
        do_callback(callback_url, failed_state)

    return log_data
