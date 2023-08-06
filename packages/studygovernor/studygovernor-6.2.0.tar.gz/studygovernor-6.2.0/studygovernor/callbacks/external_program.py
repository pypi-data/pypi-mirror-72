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

import os
import subprocess
from typing import Mapping, Sequence

from flask import current_app

from studygovernor.models import ExternalSystem


def external_program(experiment: str,
                     action_url: str,
                     binary: str,
                     args: Sequence[str]=None,
                     kwargs: Mapping[str, str]=None,
                     xnat_external_system_name: str='XNAT'):
    """
    Calls an external command. The binary gets the command in the form:

    .. code-block:: bash

       binary $ARGS $KWARGS

    :param experiment: experiment uri
    :param action_url: action url
    :param binary: binary that gets executed
    :param args: list of args [val1 val2 ...]
    :param kwargs: list of [key1 val1 key2 val2 ...]
    :param xnat_external_system_name: name of the external xnat [XNAT]

    The items in args and values in kwargs that contain certain VARS will be replaced. Accepted VARS:

    - $EXPERIMENT - will be substituted with the experiment URL.
    - $XNAT - will be substituted with the xnat URL.

    Example:

    .. code-block:: JSON

       {
         "function": "external_program",
         "binary": "check.py",
         "args": ["$EXPERIMENT"],
         "kwargs": {
           "-x": "$XNAT"
         }
       }

    """
    args = args or []
    kwargs = kwargs or {}

    # Validate the the binary is in fact in the binary dir and get full path
    binaries = os.listdir(current_app.config['STUDYGOV_PROJECT_BIN'])

    if binary not in binaries:
        raise ValueError('Cannot find binary {} in {}'.format(binary, current_app.config['STUDYGOV_PROJECT_BIN']))

    binary = os.path.join(current_app.config['STUDYGOV_PROJECT_BIN'], binary)
    
    # Get XNAT address from database
    xnat = ExternalSystem.query.filter(ExternalSystem.system_name == xnat_external_system_name).one()
    xnat_uri = xnat.url.rstrip('/')
    args = [x.replace("$XNAT", xnat_uri) for x in args]
    kwargs = {k: v.replace("$XNAT", xnat_uri) for k, v in kwargs.items()}

    # Substitute $EXPERIMENT in args and kwargs
    experiment = str(experiment)
    args = [x.replace("$EXPERIMENT", experiment) for x in args]
    kwargs = {k: v.replace("$EXPERIMENT", experiment) for k, v in kwargs.items()}

    # Build the command and execute
    command = [binary] + [str(x) for x in args] + [str(x) for k, v in kwargs.items() for x in [k, v]]

    print('Calling command: {}'.format(command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Make sure there is not stdin required and catch result
    stdout, stderr = proc.communicate()

    # Truncate stdout and stderr to be 64000 bytes together, stderr takes
    #  priority and only show the end. Use max 48000 bytes for stderr to
    # always have some space for the stdout.
    stderr = stderr[-48000:]
    stdout_len = 64000 - len(stderr)
    if stdout_len > 0:
        stdout = stdout[-stdout_len:]
    else:
        stdout = ""

    # Format return results
    return "=======\nSTDERR:\n=======\n{}\n\n=======\nSTDOUT\n=======\n{}".format(stderr, stdout)



