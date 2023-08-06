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

#!/usr/bin/env python


def run(args=None):
    import argparse
    from studygovernor import create_app

    parser = argparse.ArgumentParser(description="Run the webserver. Never use this for production!!!")
    parser.add_argument('--debug', action='store_true', default=False, help="Run the server in debug mode.")
    parser.add_argument('--host', default=None, help="Define the host, leave empty for localhost. (e.g. 0.0.0.0)")
    parser.add_argument('--port', default=None, type=int, help="Define the port, leave empty for 5000")
    args = parser.parse_args(args=args)

    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.debug)


def run_gunicorn(args=None):
    try:
        from gunicorn.app.base import BaseApplication
    except ImportError:
        print("In order to run the server with gunicorn install it with: pip install gunicorn")
        return False

    from studygovernor import create_app
    app = create_app()

    class WSGIServer(BaseApplication):
        def __init__(self, app):
            self.application = app
            super(WSGIServer, self).__init__("%(prog)s [OPTIONS]")

        def load_config(self):
            parser = self.cfg.parser()
            args = parser.parse_args()

            for k, v in args.__dict__.items():
                if v is None:
                    continue
                if k == 'args':
                    continue
                self.cfg.set(k.lower(), v)

        def load(self):
            return self.application

    WSGIServer(app).run()


def db_init(args=None):
    from studygovernor import create_app
    from studygovernor.models import db

    # Create app for the context
    app = create_app()

    # Create the database
    with app.app_context():
        db.create_all()
    #TODO implement database migration things using alembic (preferably)


def db_clean(args=None):
    import argparse
    from studygovernor import create_app
    from studygovernor.models import db

    parser = argparse.ArgumentParser(description='Clean the study governor database')
    parser.add_argument('-f', '--force', action="store_true", help="Force (do not prompt for confirmation)")
    args = parser.parse_args()

    if args.force or input("Are you sure you want to empty the database [yes/no]: ") == 'yes':
        # Create app for the context
        app = create_app()

        with app.app_context():
            db.drop_all()
            db.create_all()
        print("Database is empty!")
    else:
        print("Cancelled database clean action.")


def config_from_file(args=None):
    import argparse

    parser = argparse.ArgumentParser(description="Configure the study governor user/roles from a config json file.")
    parser.add_argument('config', metavar="JSON", help="A json file containing the config for the study governor.")
    args = parser.parse_args(args=args)

    from . import create_app
    from .util.helpers import load_config_file
    app = create_app()
    load_config_file(app, args.config)


def create_subject(args=None):
    import argparse
    import datetime
    import requests

    def to_date(value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    parser = argparse.ArgumentParser(description='Initialise the workflow: fill the DB with states and its possible transitions.')
    parser.add_argument('--host', type=str, help='The server to add the subject to', required=True)
    parser.add_argument('-l', '--label', type=str, help='The label of the subject', required=True)
    parser.add_argument('-d', '--date_of_birth', type=to_date, required=True)
    args = parser.parse_args()

    subject = {
        'label': args.label,
        'date_of_birth': str(args.date_of_birth),
    }

    server = args.host.rstrip('/')

    if input("Are you sure you want add new subject '{}' to {} [yes/no]: ".format(subject, server)) == 'yes':
        response = requests.post('{}/api/v1/subjects'.format(server), json=subject)
        print("\n * Committed to the REST api: [{}] {}.".format(response.status_code, response.text))
    else:
        print("\n * Cancelled adding the subject.")


def create_experiment(args=None):
    import argparse
    from flask_restplus import inputs
    import requests

    parser = argparse.ArgumentParser(description='Initialise the workflow: fill the DB with states and its possible transitions.')
    parser.add_argument('--host', type=str, help='The server to add the subject to', required=True)
    parser.add_argument('-l', '--label', type=str, help='The label of the experiment', required=True)
    parser.add_argument('-s', '--subject', type=str, help='The subject this experiment belongs to', required=True)
    parser.add_argument('-d', '--scandate', type=inputs.datetime_from_iso8601, help='The timestamp when the experiment was acquired', required=True)
    args = parser.parse_args()

    server = args.host.rstrip('/')
    subject = args.subject

    if not (server.startswith('http://') or server.startswith('https://')):
        server = 'http://{}'.format(server)

    if not subject.startswith('/api/v1/subjects/'):
        subject = '/api/v1/subjects/{}'.format(subject)

    experiment = {
        'label': args.label,
        'subject': subject,
        'scandate': args.scandate.isoformat(),
    }

    if input("Are you sure you want add new experiment '{}' to {} [yes/no]: ".format(experiment, server)) == 'yes':
        response = requests.post('{}/api/v1/experiments'.format(server), json=experiment)
        print("\n * Committed to the REST api: [{}] {}.".format(response.status_code, response.text))
    else:
        print("\n * Cancelled adding the subject.")


def workflow_init(args=None):
    import argparse
    from .util.helpers import initialize_workflow

    parser = argparse.ArgumentParser(description='Initialise the workflow: fill the DB with states and its possible transitions.')
    parser.add_argument('workflow', type=str, help='The workflow definition (JSON)')
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Do not ask questions, just do it")
    parser.add_argument('-u', '--upgrade', action='store_true', default=False, help="Allow for the workflow to be upgraded if already present")
    args = parser.parse_args()

    from studygovernor import create_app
    app = create_app()

    initialize_workflow(args.workflow, app=app, verbose=True, force=args.force, upgrade=args.upgrade)


def visualize_workflow(args=None):
    import argparse
    import yaml
    import os
    import subprocess

    parser = argparse.ArgumentParser(description='Plot the workflow using graphviz.')
    parser.add_argument('workflow', metavar='WORKFLOW.json', type=str, help='The workflow definition (JSON)')
    parser.add_argument('result', type=str, metavar='IMAGE.svg', help='The result image to write')
    args = parser.parse_args()

    try:
        with open(args.workflow) as fh:
            workflow_definition = yaml.safe_load(fh)
    except IOError as e:
        print("IOError: {}".format(e))
        print("Please specify a valid json file.")
        return

    style_map = {
        'external_program': 'fillcolor=darkolivegreen1',
        'send_mail': 'fillcolor=darkgreen,fontcolor=white',
        'ifdb': 'fillcolor=lightsalmon',
        'fastr': 'fillcolor=lightskyblue1',
        'create_task': 'fillcolor=lightgoldenrod1',
        'done': 'fillcolor=indigo,fontcolor=white,color=darkolivegreen1,penwidth=3.0',
        'untracked': 'fillcolor=indigo,fontcolor=white,color=plum1,penwidth=3.0',
        'unspecified': 'fillcolor=plum1',
        'failed': 'color=red,penwidth=3.0'}

    lines = ['digraph graphname { node [shape=box,style=filled,fillcolor=white,margin="0.45,0.055"]; ']

    # Create a legend
    lines.append('subgraph cluster_legend { color=black label=Legend ')
    for function, style in style_map.items():
        lines.append(' "{function} node" [label="{function} node",{style},]; '.format(function=function, style=style))
    for x, y in zip(style_map.keys(), list(style_map.keys())[1:]):
        lines.append(' "{} node" -> "{} node" [color=invis];'.format(x, y))
    lines.append("}")
    
    # Generate the states nodes
    for nr, s in enumerate(workflow_definition['states']):
        extra_attrs = ""
        if s['callback'] is not None:
            extra_attrs += "{style},".format(style=style_map.get(s['callback']['function'], style_map['unspecified']))
        if 'failed' in s['label']:
            extra_attrs += style_map['failed']
        if s['label'] in list(style_map.keys()):
            extra_attrs += "{},".format(style_map[s['label']])
        lines.append('  "{label}" [label="{id}: {label}",{extra}];'.format(id=nr+1, label=s['label'], extra=extra_attrs))

    # Generate all transitions between the states
    for nr, t in enumerate(workflow_definition['transitions']):
        lines.append('  "{}" -> "{}" [label="{}"];'.format(t["source"], t["destination"], nr+1))

    # Close the digraph
    lines.append('}')

    image_file_path = args.result
    dot_file_path, img_format = os.path.splitext(args.result)
    dot_file_path += '.dot'

    print('Using {} as intermediate file'.format(dot_file_path))
    with open(dot_file_path, 'w') as output_file:
        for line in lines:
            output_file.write(line)
            output_file.write('\n')

    try:
        img_format = img_format.strip('.')
        print('Using image format: {}'.format(img_format))
        proc = subprocess.Popen(['dot', '-T{}'.format(img_format), '-o{}'.format(image_file_path), dot_file_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        print('Subprocess call to do finished with stdout: {}, stderr: {}'.format(stdout, stderr))

        if not os.path.exists(image_file_path):
            print('Network draw failed the graphviz coversion:\n{}'.format(stdout))
        print("converted to %s", image_file_path)
        return image_file_path
    except OSError:
        print("Cannot convert %s to an svg image. Please put dot (from GraphViz) in your PATH.", image_file_path)
        return None
    finally:
        if os.path.isfile(dot_file_path):
            os.remove(dot_file_path)


def flask_manager(args=None):
    from flask_script import Manager
    from flask_migrate import Migrate, MigrateCommand

    from studygovernor import create_app
    from studygovernor.models import db

    app = create_app(use_sentry=False)
    migrate = Migrate()
    migrate.init_app(app=app, db=db, directory='migrations')
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()


def run_callback():
    import argparse
    import sys

    from urllib.parse import urlparse


    parser = argparse.ArgumentParser(description='Run a callback')
    parser.add_argument('-u', '--action_url', type=str, help="URL of the action related to the callback", required=True)
    parser.add_argument('-c', '--callback_data', type=str, help="JSON String with callback data", required=False)
    args = parser.parse_args()

    from studygovernor import create_app
    from studygovernor import models
    action_id = None

    app = create_app()

    if args.action_url:
        parts = args.action_url.split('/')
        if parts[-2] == 'actions': # get action id from url
            action_id = int(parts[-1])

    if action_id is None:
        print('Invalid action url {}'.format(args.action_url))
        sys.exit(-1)

    with app.app_context():
        action = models.db.session.query(models.Action).filter(models.Action.id == action_id).first()

        if not action:
            print('No action found for action {}'.format(args.action_url))
            sys.exit(-1)

        from studygovernor.callbacks import master_callback

        # Use callback data
        if args.callback_data is None:
            callback_data = action.transition.destination_state.callback
        else:
            callback_data = args.callback_data

        master_callback(callback_data, args.action_url)


if __name__ == "__main__":
    import sys
    sys.exit("This is where entry points are defined. Look for studygov-* executables on the path.")
