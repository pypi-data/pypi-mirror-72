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

import pathlib
import pytest

from . import create_app


@pytest.fixture(scope="module")
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_uri = 'sqlite:///:memory:'

    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SECRET_KEY': 'o8[nc2foeu2foe2ij',
        'SECURITY_PASSWORD_SALT': 'sgfms8-tcfm9de2nv'
    }, use_sentry=False)
    with app.app_context():
        yield app


@pytest.fixture(scope="function")
def init_db(app):
    # create the database and load test data
    from .models import db
    db.create_all(app=app)

    yield db

    db.drop_all()
    db.session.commit()


@pytest.fixture(scope="function")
def app_config(app, init_db):
    # Load the config file with initial setup
    config_file = pathlib.Path(__file__).parent / 'tests' / 'config' / 'test_config.yaml'
    from .util.helpers import load_config_file
    load_config_file(app, config_file, silent=True)


@pytest.fixture(scope="function")
def workflow_test_data(app, app_config):
    # Load test workflow
    workflow_file = pathlib.Path(__file__).parent / 'tests' / 'test_workflow.yaml'

    # Make sure the workflow is loaded
    from .util.helpers import initialize_workflow
    initialize_workflow(workflow_file, app=app)


@pytest.fixture(scope="function")
def second_workflow_test_data(app, init_db, app_config):
    # Load test workflow
    workflow_file = pathlib.Path(__file__).parent / 'tests' / 'second_workflow.yaml'

    # Make sure the workflow is loaded
    from .util.helpers import initialize_workflow
    initialize_workflow(workflow_file, app=app)


@pytest.fixture(scope="function")
def subject_data(init_db):
    from datetime import date
    from studygovernor.models import Subject
    from studygovernor.models import db

    # Create 2 test subjects
    for subject_id in range(1, 3):
        subject_label = f"Test Subject_{subject_id}"
        subject_dob = date(2019, 1, subject_id)
        subject = Subject(label=subject_label, date_of_birth=subject_dob)
        db.session.add(subject)
        db.session.commit()


@pytest.fixture(scope="function")
def experiment_data(subject_data, workflow_test_data):
    from datetime import date
    from studygovernor.models import Subject
    from studygovernor.models import Experiment
    from studygovernor.models import db
    from studygovernor.models import Workflow

    workflows = Workflow.query.all()
    print(f"workflows found: {len(workflows)}")
    for workflow in workflows:
        print(workflow)

    workflow = Workflow.query.order_by(Workflow.id.desc()).first()

    # Create 2 test experiments per test subject
    subjects = Subject.query.filter(Subject.label.startswith('Test Subject_')).all()
    for subject in subjects:
        for experiment_id in range(1, 3):
            experiment_label = f"Experiment_{subject.id}_{experiment_id}"
            experiment_scandate = date(2019, 1, experiment_id)
            experiment = Experiment(workflow, subject=subject, label=experiment_label, scandate=experiment_scandate)
            db.session.add(experiment)
            db.session.commit()


@pytest.fixture(scope="function")
def externalsystem(init_db):
    from studygovernor.models import ExternalSystem
    from studygovernor.models import db
    # Create 3 external systems
    for externalsystem_id in range(1, 4):
        system_name = f'NewSystemName_{externalsystem_id}'
        system_url = f'http://system-{externalsystem_id}.url'

        external_system = ExternalSystem(system_name=system_name, url=system_url)
        db.session.add(external_system)
    db.session.commit()


@pytest.fixture(scope="function")
def subject_links(subject_data, externalsystem):
    # Link External systems to Subject
    from studygovernor.models import ExternalSystem
    from studygovernor.models import Subject
    from studygovernor.models import ExternalSubjectLinks
    from studygovernor.models import db

    # Get data
    subjects = Subject.query.all()
    externalsystems = ExternalSystem.query.all()

    # Define links
    externalsystem_links = [
        (externalsystems[0], subjects[0], 1),  # Link externalsystem[0] to subject[0]
        (externalsystems[1], subjects[1], 2),  # Link externalsystem[1] to subject[1]
        (externalsystems[2], subjects[1], 2),  # Link externalsystem[2] to subject[1]
    ]

    # link subjects to external_data
    for externalsystem_link in externalsystem_links:
        external_link = ExternalSubjectLinks(
            f'External_SubjectID_{externalsystem_link[2]}',
            externalsystem_link[1],
            external_system=externalsystem_link[0])
        db.session.add(external_link)
    db.session.commit()


@pytest.fixture(scope="function")
def experiment_links(experiment_data, externalsystem):
    # Link External systems to Subject
    from studygovernor.models import ExternalSystem
    from studygovernor.models import Experiment
    from studygovernor.models import ExternalExperimentLinks
    from studygovernor.models import db

    # Get data
    experiments = Experiment.query.all()
    externalsystems = ExternalSystem.query.all()

    # Define links
    externalsystem_links = [
        (externalsystems[0], experiments[0], 1),  # Link externalsystem[0] to subject[0]
        (externalsystems[1], experiments[1], 2),  # Link externalsystem[1] to subject[0]
        (externalsystems[2], experiments[1], 2),  # Link externalsystem[3] to subject[0]
    ]

    # link experiments to external_data
    for externalsystem_link in externalsystem_links:
        external_link = ExternalExperimentLinks(
            f'External_ExperimentID_{externalsystem_link[2]}',
            externalsystem_link[1],
            external_system=externalsystem_link[0])
        db.session.add(external_link)
    db.session.commit()


@pytest.fixture
def client(app, app_config):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="module")
def no_db_app():
    """ Create and configure a new app instance with an invalid database. """
    db_uri = 'mysql+pymysql://user:password@localhost/non_existing_db'

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SECRET_KEY': 'o8[nc2foeu2foe2ij',
        'SECURITY_PASSWORD_SALT': 'sgfms8-tcfm9de2nv'
    }, use_sentry=False)

    yield app


@pytest.fixture
def no_db_client(no_db_app):
    """ A test client without a db. """
    return no_db_app.test_client()
