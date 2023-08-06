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
import yaml

from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password

from .. import models
from .. import exceptions


def load_config_file(app, file_path, silent=False):
    file_path = str(file_path)

    with app.app_context():
        db = models.db

        user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
        if not os.path.isfile(file_path):
            db.session.rollback()
            raise ValueError(f"The file ({file_path}) does not exist")

        basedir = os.path.dirname(os.path.abspath(file_path))
        with open(file_path) as fh:
            config = yaml.safe_load(fh)

        if 'roles' in config:
            if not silent:
                print("\n Adding Roles:")
            roles = {}
            for role in config["roles"]:
                roles[role['name']] = user_datastore.create_role(**role)
                if not silent:
                    print(f"{roles[role['name']]} {role}")
            db.session.commit()

        if 'users' in config:
            if not silent:
                print("\nAdding users:")
            for user in config['users']:
                user['password'] = hash_password(user['password'])
                db_user = user_datastore.create_user(**user)
                if not silent:
                    print(f"Adding {db_user}")
            db.session.commit()

        print("\nAdding external_systems:")
        for experiment in config.get('external_systems', []):
            db.session.add(models.ExternalSystem(system_name=experiment['system_name'], url=experiment['url']))
            print(f"Adding {experiment['system_name']}")

        print("\nAdding scantypes:")
        for scan_type in config.get('scantypes', []):
            db.session.add(models.Scantype(modality=scan_type['modality'], protocol=scan_type['protocol']))
            print(f"Adding {scan_type['modality']} {scan_type['protocol']}")

        if not silent:
            print("\nCommitting to the database ...")
        db.session.commit()
        if not silent:
            print("[ DONE ]")


def get_object_from_arg(id, model, model_name=None, skip_id=False, allow_none=False, filters=None):
    # Set initial return data to None already
    data = None

    # Check if id is already a valid instance of model
    if isinstance(id, model):
        return id

    if id is not None:
        # If we have a URI/path we just want the last part
        if isinstance(id, str) and '/' in id:
            id = id.rsplit('/', 1)[1]

        # For id try to cast to an int
        if not skip_id:
            try:
                id = int(id)
            except (TypeError, ValueError) as e:
                pass

        # Create base query
        if isinstance(id, int):
            query = model.query.filter(model.id == id)
        elif model_name is not None:
            query = model.query.filter(model_name == id)
        else:
            query = None
        
        # If there is a query, add filters and run query
        if query is not None:
            if filters is not None:
                for key, value in filters.items():
                    query = query.filter(key == value)
                
            data = query.one_or_none()
        
    # Check if there is data or None is allowed
    if data is None and not allow_none:
        raise exceptions.CouldNotFindResourceError(id, model)

    return data


def initialize_workflow(workflow, app, verbose=False, force=True, upgrade=False):
    from pathlib import Path
    from .. import models

    if isinstance(workflow, (str, Path)):
        try:
            with open(workflow) as fh:
                workflow_definition = yaml.safe_load(fh)
        except IOError as experiment:
            print("IOError: {}".format(experiment))
            print("Please specify a valid YAML file.")
            return
    else:
        workflow_definition = workflow

    if verbose:
        def do_print(message):
            print(message)
    else:
        def do_print(message):
            pass

    with app.app_context():
        db = models.db

        try:
            workflow_label = workflow_definition['label']
        except KeyError:
            print(f'[ERROR] Workflow definition should contain a label to manage multiple version!')
            return

        workflow = models.Workflow.query.filter(models.Workflow.label == workflow_label).one_or_none()

        if workflow is None:
            workflow = models.Workflow(label=workflow_label)
        else:
            if upgrade:
                print(f"[WARNING] Upgrading workflows is currently not supported!")
                return

                # TODO: For upgrading, we should not only delete, but make a delta,
                # check if delete is safe, delete using hide flag (for history),
                # create new states and transitions. Quite a project. :-)
                # print(f"Upgrading workflow {workflow_label} with new data")
                # old_states = models.State.query().filter(models.State.workflow == workflow)
                # old_transitions = models.Transition.query(models.Transition.source_state.in_(old_states.subquery()))
                # old_transitions.delete()
                # old_states.delete()
            else:
                print(f'[ERROR] Workflow with label {workflow_label} already exists, use the upgrade flag to upgrade!')
                return

        do_print("\n * Importing states:")
        states = dict()
        for state in workflow_definition['states']:
            callback = state['callback']

            # Allow callback to be defined as nested JSON rather than a string containing escaped JSON
            if not isinstance(callback, str) and callback is not None:
                callback = yaml.safe_dump(callback)

            states[state['label']] = models.State(label=state['label'],
                                                  lifespan=state['lifespan'],
                                                  callback=callback,
                                                  freetext=state['freetext'],
                                                  workflow=workflow)
            db.session.add(states[state['label']])
            do_print("\t - {}".format(state['label']))

        do_print("\n * Importing transitions:")
        for transition in workflow_definition['transitions']:
            #TODO add conditions
            db.session.add(models.Transition(source_state=states[transition['source']], destination_state=states[transition['destination']]))
            do_print("\t - {} -> {}".format(transition['source'], transition['destination']))

        if 'external_systems' in workflow_definition:
            print("[WARNING] External systems are no longer defined as part of a workflow, "
                  "but as part of the config! Ignoring external_systems section")

        if 'scantypes' in workflow_definition:
            print("[WARNING] Scantypes are no longer defined as part of a workflow, "
                  "but as part of the config! Ignoring scantypes section")

        doit = False
        if not force:
            doit = input("Are you sure you want to commit this to '{}' [yes/no]: ".format(app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)[1])) == 'yes'

        if doit or force:
            db.session.commit()
            do_print("\n * Committed to the database.")
        else:
            db.session.rollback()
            do_print("\n * Cancelled the initialisation of the workflows.")
