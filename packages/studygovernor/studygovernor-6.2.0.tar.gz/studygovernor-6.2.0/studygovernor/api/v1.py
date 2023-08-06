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

from flask import Blueprint, abort, url_for, current_app
from flask_restplus import Api, Resource, reqparse, fields, inputs, marshal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from flask_security import auth_required, current_user, http_auth_required, permissions_accepted, permissions_required
from flask_security.utils import hash_password

from . import RegisteredApi
from .. import exceptions
from .. import models
from .. import user_datastore
from ..fields import ObjectUrl, SubUrl, MappingField
from ..models import db
from ..util.helpers import get_object_from_arg

blueprint = Blueprint('api_v1', __name__)

api = RegisteredApi(
    blueprint,
    version='1.0',
    title='Study Governor REST API version 1.0',
    description='The Study Governor is for tracking experiments and study resources.',
    default_mediatype='application/json'
)


action_list = api.model('ActionList', {
    'actions': fields.List(ObjectUrl('api_v1.action', attribute='id'))
})


def has_permission_any(*args):
    return any(current_user.has_permission(perm) for perm in args)


def has_permission_all(*args):
    return all(current_user.has_permission(perm) for perm in args)


@api.route('/actions', endpoint='actions')
class ActionListAPI(Resource):
    @http_auth_required
    @api.marshal_with(action_list)
    @api.response(200, 'Success')
    def get(self):
        actions = models.Action.query.all()
        return {'actions': actions}


action_get = api.model('ActionGet', {
    'uri': fields.Url,
    'experiment': ObjectUrl('api_v1.experiment', attribute='experiment_id'),
    'transition': ObjectUrl('api_v1.transition', attribute='transition_id'),
    'success': fields.Boolean,
    'return_value': fields.String,
    'freetext': fields.String,
    'start_time': fields.DateTime(dt_format='iso8601'),
    'end_time': fields.DateTime(dt_format='iso8601'),
})


action_put = api.model('ActionPut', {
    'success': fields.Boolean,
    'return_value': fields.String,
    'end_time': fields.DateTime(dt_format='iso8601'),
})


@api.route('/actions/<int:id>', endpoint='action')
class ActionAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('success', type=bool, required=False, location='json')
    request_parser.add_argument('return_value', type=str, required=False, location='json')
    request_parser.add_argument('end_time', type=inputs.datetime_from_iso8601, required=False, location='json')

    @http_auth_required
    @api.marshal_with(action_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find action')
    def get(self, id: int):
        action = models.Action.query.filter(models.Action.id == id).one_or_none()
        if action is None:
            abort(404)
        return action

    @http_auth_required
    @permissions_accepted('action_update')
    @api.marshal_with(action_get)
    @api.expect(action_put)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find action')
    def put(self, id: int):
        action = models.Action.query.filter(models.Action.id == id).one_or_none()
        if action is None:
            abort(404)

        args = self.request_parser.parse_args()

        if 'success' in args:
            action.success = args['success']

        if 'return_value' in args:
            action.return_value = args['return_value']

        if 'end_time' in args:
            action.end_time = args['end_time']

        db.session.commit()
        db.session.refresh(action)

        return action


condition_list = api.model('ConditionList', {
    'conditions': fields.List(ObjectUrl('api_v1.condition', attribute='id'))
})


@api.route('/conditions', endpoint='conditions')
class ConditionListAPI(Resource):
    @http_auth_required
    @api.marshal_with(condition_list)
    @api.response(200, 'Success')
    def get(self):
        conditions = models.Condition.query.all()
        return {'conditions': conditions}


condition_get = api.model('ConditionGet', {
    'uri': fields.Url,
    'rule': fields.String,
    'freetext': fields.String,
})


@api.route('/conditions/<int:id>', endpoint='condition')
class ConditionAPI(Resource):
    @http_auth_required
    @api.marshal_with(condition_get)
    @api.response(200, 'Success')
    def get(self, id: int):
        condition = models.Condition.query.filter(models.Condition.id == id).one_or_none()
        if condition is None:
            abort(404)
        return condition


experiment_list = api.model('ExperimentList', {
    'experiments': fields.List(ObjectUrl('api_v1.experiment', attribute='id'))
})


experiment_get = api.model('ExperimentGet', {
    'uri': fields.Url('api_v1.experiment'),
    'subject': ObjectUrl('api_v1.subject', attribute='subject_id'),
    'label': fields.String,
    'scandate': fields.DateTime(dt_format='iso8601'),
    'state': SubUrl('api_v1.experiment', 'state', attribute='id'),
    'external_ids': MappingField
})


experiment_post = api.model('ExperimentPost', {
    'subject': ObjectUrl('api_v1.subject', attribute='subject_id'),
    'label': fields.String,
    'scandate': fields.DateTime(dt_format='iso8601'),
})


@api.route('/experiments', endpoint='experiments')
class ExperimentListAPI(Resource):
    # Request parser for the get function when filtering
    get_request_parser = reqparse.RequestParser()
    get_request_parser.add_argument('scandate', type=inputs.datetime_from_iso8601, required=False,
                                    location='args')
    get_request_parser.add_argument('subject', type=str, required=False,
                                    location='args')
    get_request_parser.add_argument('state', type=str, required=False,
                                    location='args')

    # Request parser for when adding an experiment
    post_request_parser = reqparse.RequestParser()
    post_request_parser.add_argument('label', type=str, required=True, location='json',
                                     help='No label supplied')
    post_request_parser.add_argument('scandate', type=inputs.datetime_from_iso8601, required=True,
                                     location='json', help='No scandate supplied')
    post_request_parser.add_argument('subject', type=str, required=True, location='json',
                                     help='No subject supplied')
    post_request_parser.add_argument('workflow', type=str, required=False, location='json')

    @http_auth_required
    @api.marshal_with(experiment_list)
    @api.response(200, 'Success')
    def get(self):
        args = self.get_request_parser.parse_args()
        query = models.Experiment.query

        if args['subject'] is not None:
            query = query.filter(models.Experiment.subject_id == args['subject'])

        if args['scandate'] is not None:
            query = query.filter(models.Experiment.scandate == args['scandate'])

        experiments = query.all()

        # This should move to the DB if possible, but querying on state is problematic
        if args['state'] is not None:
            try:
                state = int(args['state'])
                experiments = [x for x in experiments if x.state.id == state]
            except ValueError:
                experiments = [x for x in experiments if x.state.label == args['state']]

        return {'experiments': experiments}

    @http_auth_required
    @permissions_required('sample_add')
    @api.marshal_with(experiment_get)
    @api.expect(experiment_post)
    @api.response(201, 'Created experiment')
    @api.response(404, 'Could not find specified subject')
    def post(self):
        args = self.post_request_parser.parse_args()

        # Find the id for the subject url
        subject = get_object_from_arg(args['subject'], models.Subject, models.Subject.label)
        if args['workflow'] is not None:
            workflow = get_object_from_arg(args['workflow'], models.Workflow, models.Workflow.label)
        else:
            workflow = models.Workflow.query.order_by(models.Workflow.id.desc()).first()

        # Post the experiment
        print('[DEBUG] Creating experiment {}'.format(args['label']))
        experiment = models.Experiment(workflow, label=args['label'], scandate=args['scandate'], subject=subject)
        db.session.add(experiment)
        db.session.commit()
        db.session.refresh(experiment)
        print('[DEBUG] EXPERIMENT: {}'.format(experiment.id))

        return experiment, 201


@api.route('/experiments/<id>', endpoint='experiment')
class ExperimentAPI(Resource):
    @http_auth_required
    @api.marshal_with(experiment_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find experiment')
    def get(self, id):
        try:
            id = int(id)
            experiment = models.Experiment.query.filter(models.Experiment.id == id).one_or_none()
        except ValueError:
            experiment = models.Experiment.query.filter(models.Experiment.label == id).one_or_none()

        if experiment is None:
            abort(404)
        return experiment


experiment_state_model = api.model('State', {
    'state': ObjectUrl('api_v1.state', attribute='id'),
    'workflow': ObjectUrl('api_v1.workflow', attribute='workflow_id'),

})

experiment_state_put_args = api.model('StatePutArgs', {
    'state': fields.String,
    'freetext': fields.String
})

experiment_state_put = api.model('StatePut', {
    'state': ObjectUrl('api_v1.state'),
    'error': fields.Raw,
    'success': fields.Boolean,
})


@api.route('/experiments/<int:id>/actions', endpoint='experiment_actions')
class ActionListAPI(Resource):
    @http_auth_required
    @api.marshal_with(action_list)
    @api.response(200, 'Success')
    def get(self, id: int):
        actions = models.Action.query.filter(models.Action.experiment_id == id).all()
        return {'actions': actions}


@api.route('/experiments/<int:id>/state', endpoint='experiment_state')
class ExperimentStateAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('state', type=str, required=True, location='json',
                                help='No state supplied')
    request_parser.add_argument('freetext', type=str, required=False, location='json',
                                help='Free text annotation for the created action')

    @http_auth_required
    @api.marshal_with(experiment_state_model)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified experiment')
    def get(self, id: int):
        experiment = get_object_from_arg(id, models.Experiment, models.Experiment.label)

        return experiment.state

    @http_auth_required
    @permissions_required('sample_state_update')
    @api.marshal_with(experiment_state_put)
    @api.expect(experiment_state_put_args)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified state')
    @api.response(409, 'Cannot change state to specified state, no valid transition!')
    def put(self, id):
        experiment = get_object_from_arg(id, models.Experiment, models.Experiment.label)
        current_workflow = experiment.state.workflow

        args = self.request_parser.parse_args()
        
        state = get_object_from_arg(
            args['state'],
            models.State,
            models.State.label, allow_none=True,
            filters={models.State.workflow: current_workflow}
        )

        if state is None:
            success = False
            error = {
                'errorclass': 'StateNotFoundError',
                'requested_state': args['state'],
                'message': 'Could not find requested state "{}"'.format(args['state']),
            }
            status = 404
        else:
            # Try to change the state
            try:
                experiment.set_state(state, 'api_v1', args['freetext'])
                success = True
                error = None
                status = 200
            except exceptions.StateChangeError as err:
                success = False
                error = err.marshal(api_prefix='api_v1')
                status = 409

        data = {
            'state': experiment.state.id,
            'error': error,
            'success': success,
        }

        print(experiment.state)

        return data, status


external_systems = api.model('ExternalSystems', {
    'external_systems': fields.List(ObjectUrl('api_v1.external_system', attribute='id'))
})


@api.route('/external_systems', endpoint='external_systems')
class ExternalSystemListAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_systems)
    @api.response(200, 'Success')
    def get(self):
        external_systems = models.ExternalSystem.query.all()
        return {'external_systems': external_systems}


external_system_model = api.model('ExternalSystem', {
    'uri': fields.Url('api_v1.external_system'),
    'url': fields.String,
    'system_name': fields.String,
})


@api.route('/external_systems/<id>', endpoint='external_system')
class ExternalSystemAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_system_model)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external system')
    def get(self, id):
        external_system = get_object_from_arg(id, models.ExternalSystem, models.ExternalSystem.system_name)

        if external_system is None:
            abort(404)
        return external_system


external_subject_links = api.model('ExternalSubjectLinks', {
    'external_subject_links': fields.List(ObjectUrl('api_v1.external_subject_link', attribute='id'))
})


external_subject = api.model('ExternalSubjectLinksGet', {
    'uri': fields.Url,
    'subject': ObjectUrl('api_v1.subject', attribute='subject_id'),
    'external_system': ObjectUrl('api_v1.external_system', attribute='external_system_id'),
    'external_id': fields.String,
})

external_subject_links_post = api.model('ExternalSubjectLinksPost', {
    'subject': fields.String,
    'external_system': fields.String,
    'external_id': fields.String,
})


@api.route('/external_subject_links', endpoint='external_subject_links')
class ExternalSubjectListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('subject', type=str, required=True, location='json',
                                help='No subject supplied')
    request_parser.add_argument('external_system', type=str, required=True, location='json',
                                help='No external system supplied')
    request_parser.add_argument('external_id', type=str, required=True, location='json',
                                help='No external id supplied')

    @http_auth_required
    @api.marshal_with(external_subject_links)
    @api.response(200, 'Success')
    def get(self):
        external_subject_links = models.ExternalSubjectLinks.query.all()
        return {'external_subject_links': external_subject_links}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(external_subject)
    @api.expect(external_subject_links_post)
    @api.response(201, 'Created')
    def post(self):
        args = self.request_parser.parse_args()

        subject = get_object_from_arg(args['subject'], models.Subject, models.Subject.label)
        external_system = get_object_from_arg(args['external_system'], models.ExternalSystem, models.ExternalSystem.system_name)

        external_subject_link = models.ExternalSubjectLinks(args['external_id'],
                                                            subject=subject,
                                                            external_system=external_system)

        db.session.add(external_subject_link)
        try:
            db.session.commit()
            db.session.refresh(external_subject_link)
        except IntegrityError:
            # This is thrown because of a duplicate external_experiment_link for the same system.
            # Rollback and fetch the original to be returned
            db.session.rollback()
            external_subject_link = models.ExternalSubjectLinks.query.filter_by(external_id=args['external_id']).one()

        return external_subject_link, 201


@api.route('/external_subject_links/<int:id>', endpoint='external_subject_link')
class ExternalSubjectAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_subject)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external subject')
    def get(self, id: int):
        external_subject_link = models.ExternalSubjectLinks.query.filter(models.ExternalSubjectLinks.id == id).one_or_none()
        if external_subject_link is None:
            abort(404)
        return external_subject_link


external_experiment_links = api.model('ExternalExperimentLinks', {
    'external_experiment_links': fields.List(ObjectUrl('api_v1.external_experiment_link', attribute='id'))
})


external_experiment_links_post = api.model('ExternalExperimentLinksPost', {
    'experiment': fields.String,
    'external_system': fields.String,
    'external_id': fields.String,
})


external_experiment = api.model('ExternalExperiment', {
    'uri': fields.Url,
    'experiment': ObjectUrl('api_v1.experiment', attribute='experiment_id'),
    'external_system': ObjectUrl('api_v1.external_system', attribute='external_system_id'),
    'external_id': fields.String,
})


@api.route('/external_experiment_links', endpoint='external_experiment_links')
class ExternalExperimentListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('experiment', type=str, required=True, location='json',
                                help='No experiment supplied')
    request_parser.add_argument('external_system', type=str, required=True, location='json',
                                help='No external system supplied')
    request_parser.add_argument('external_id', type=str, required=True, location='json',
                                help='No external id supplied')

    @http_auth_required
    @api.marshal_with(external_experiment_links)
    @api.response(200, 'Success')
    def get(self):
        external_experiment_links = models.ExternalExperimentLinks.query.all()
        return {'external_experiment_links': external_experiment_links}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(external_experiment)
    @api.expect(external_experiment_links_post)
    @api.response(201, 'Created')
    def post(self):
        args = self.request_parser.parse_args()

        # Find the the experiment to link to
        experiment = get_object_from_arg(args['experiment'], models.Experiment, models.Experiment.label)
        external_system = get_object_from_arg(args['external_system'], models.ExternalSystem, models.ExternalSystem.system_name)

        external_experiment_link = models.ExternalExperimentLinks(args['external_id'],
                                                                  experiment=experiment,
                                                                  external_system=external_system)

        db.session.add(external_experiment_link)
        try:
            db.session.commit()
            db.session.refresh(external_experiment_link)
        except IntegrityError:
            # This is thrown because of a duplicate external_system_link for the same system.
            # Rollback and fetch the original to be returned
            db.session.rollback()
            external_experiment_link = models.ExternalExperimentLinks.query.filter_by(external_id=args['external_id']).one()
            
        return external_experiment_link, 201


@api.route('/external_experiment_links/<int:id>', endpoint='external_experiment_link')
class ExternalExperimentAPI(Resource):
    @http_auth_required
    @api.marshal_with(external_experiment)
    @api.response(200, 'Success')
    @api.response(404, 'Cannot find specified external experiment')
    def get(self, id: int):
        external_experiment_link = models.ExternalExperimentLinks.query.filter(models.ExternalExperimentLinks.id == id).one_or_none()
        if external_experiment_link is None:
            abort(404)
        return external_experiment_link


scan_list = api.model('ScanList', {
    'scans': fields.List(ObjectUrl('api_v1.scan', attribute='id'))
})

scan_get = api.model('ScanGet', {
    'uri': fields.Url,
    'scantype': ObjectUrl('api_v1.scantype', attribute='scantype_id')
})


@api.route('/scans', endpoint='scans')
class ScanListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('scantype', type=str, required=True, location='json',
                                help='No label specified')
    request_parser.add_argument('experiment', type=str, required=True, location='json',
                                help='No date_of_birth specified')

    @http_auth_required
    @api.marshal_with(scan_list)
    @api.response(200, 'Success')
    def get(self):
        scans = models.Scan.query.all()
        return {'scans': scans}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(scan_get)
    @api.response(201, 'Created')
    def post(self):
        args = self.request_parser.parse_args()

        # Find the id for the subject url
        experiment = args['experiment']
        experiment = get_object_from_arg(experiment, models.Experiment, models.Experiment.label)

        # Find the id for the subject url
        scantype = args['scantype']
        scantype = get_object_from_arg(scantype, models.Scantype, models.Scantype.protocol)

        scan = models.Scan(experiment=experiment, scantype=scantype)

        db.session.add(scan)
        db.session.commit()
        db.session.refresh(scan)

        return scan, 201


@api.route('/scans/<int:id>', endpoint='scan')
class ScanAPI(Resource):
    pass


scan_type_list = api.model('ScanTypeList', {
    'scantypes': fields.List(ObjectUrl('api_v1.scantype', attribute='id'))
})


@api.route('/scantypes', endpoint='scantypes')
class ScantypeListAPI(Resource):
    @http_auth_required
    @api.marshal_with(scan_type_list)
    @api.response(200, 'Success')
    def get(self):
        scantypes = models.Scantype.query.all()
        return {'scantypes': scantypes}


scan_type = api.model('ScanType', {
    'uri': fields.Url,
    'modality': fields.String,
    'protocol': fields.String,
})


@api.route('/scantypes/<int:id>', endpoint='scantype')
class ScantypeAPI(Resource):
    @http_auth_required
    @api.marshal_with(scan_type)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified scantype')
    def get(self, id):
        scantype = models.Scantype.query.filter(models.Scantype.id == id).one_or_none()
        if scantype is None:
            abort(404)
        return scantype


state_list = api.model('StateList', {
    'states': fields.List(ObjectUrl('api_v1.state', attribute='id'))
})


@api.route('/states', endpoint='states')
class StateListAPI(Resource):
    @http_auth_required
    @api.marshal_with(state_list)
    @api.response(200, 'Success')
    def get(self):
        states = models.State.query.all()
        return {'states': states}


state_model = api.model('State', {
    'uri': fields.Url,
    'label': fields.String,
    'callback': fields.String,
    'lifespan': fields.Integer,
    'freetext': fields.String,
    'workflow': ObjectUrl('api_v1.workflow', attribute='workflow_id'),
    'experiments': SubUrl('api_v1.state', 'experiments', attribute='id')
})


@api.route('/states/<id>', endpoint='state')
class StateAPI(Resource):
    @http_auth_required
    @api.marshal_with(state_model)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified state')
    def get(self, id=None):
        state = get_object_from_arg(id, models.State, models.State.label)
        return state


@api.route('/states/<id>/experiments', endpoint='state_experiments')
class StateExperimentsAPI(Resource):
    @http_auth_required
    @api.marshal_with(experiment_list)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified state')
    def get(self, id=None):
        try:
            id = int(id)
            state = models.State.query.filter(models.State.id == id).one_or_none()
        except ValueError:
            state = models.State.query.filter(models.State.label == id).one_or_none()

        if state is None:
            abort(404)
        return {'experiments': state.experiments}


subject_list = api.model('SubjectList', {
    'subjects': fields.List(ObjectUrl('api_v1.subject', attribute='id'))
})

subject_get = api.model('SubjectGet', {
    'uri': fields.Url('api_v1.subject'),
    'label': fields.String,
    'date_of_birth': fields.String,
    'external_ids': MappingField,
    'experiments': fields.List(ObjectUrl('api_v1.experiment', attribute='id'))
})


subject_post = api.model('SubjectPost', {
    'label': fields.String,
    'date_of_birth': fields.String,
})


@api.route('/subjects', endpoint='subjects')
class SubjectListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('label', type=str, required=True, location='json',
                                help='No label specified')
    request_parser.add_argument('date_of_birth', type=inputs.date, required=True, location='json',
                                help='No date_of_birth specified')

    @http_auth_required
    @api.marshal_with(subject_list)
    @api.response(200, 'Success')
    def get(self):
        subjects = models.Subject.query.all()
        return {'subjects': subjects}

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(subject_get)
    @api.expect(subject_post)
    @api.response(201, 'Created')
    def post(self):
        current_app.logger.info("[INFO] About to post subject!")
        subject = models.Subject(**self.request_parser.parse_args())
        db.session.add(subject)
        db.session.commit()
        db.session.refresh(subject)

        return subject, 201


@api.route('/subjects/<id>', endpoint='subject')
class SubjectAPI(Resource):
    request_parser_get = api.parser()
    request_parser_get.add_argument('filter_field', type=str, required=False, location='args', help='Should be either "id" or "label"')

    request_parser_post = reqparse.RequestParser()
    request_parser_post.add_argument('label', type=str, required=False, location='json')
    request_parser_post.add_argument('date_of_birth', type=inputs.date, required=False, location='json')

    @http_auth_required
    @api.marshal_with(subject_get)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified subject')
    @api.expect(request_parser_get)
    def get(self, id):
        args = self.request_parser_get.parse_args()
        if args['filter_field'] == 'id':
            try:
                id_ = int(id)
                subject = models.Subject.query.filter(models.Subject.id == id_).one_or_none()
            except ValueError as excp:
                print(excp)
                subject = None
        elif args['filter_field'] == 'label':
            label = str(id)
            subject = models.Subject.query.filter(models.Subject.label == label).one_or_none()
        else:
            try:
                id_ = int(id)
                subject = models.Subject.query.filter(models.Subject.id == id_).one()
            except (ValueError, NoResultFound):
                label = str(id)
                subject = models.Subject.query.filter(models.Subject.label == label).one_or_none()

        if subject is None:
            abort(404)
        return subject

    @http_auth_required
    @permissions_accepted('sample_add')
    @api.marshal_with(subject_get)
    @api.expect(subject_post)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified subject')
    def put(self, id):
        args = self.request_parser_post.parse_args()
        subject = models.Subject.query.filter(models.Subject.id == id).one_or_none()

        if subject is None:
            abort(404)

        if args.get('label') is not None:
            subject.label = args['label']
        if args.get('date_of_birth') is not None:
            subject.date_of_birth = args['date_of_birth']

        db.session.commit()
        db.session.refresh(subject)

        return subject


transition_list = api.model('TransitionList', {
    'transitions': fields.List(ObjectUrl('api_v1.transition', attribute='id'))
})


@api.route('/transitions', endpoint='transitions')
class TransitionListAPI(Resource):
    @http_auth_required
    @api.marshal_with(transition_list)
    @api.response(200, 'Success')
    def get(self):
        transitions = models.Transition.query.all()
        return {'transitions': transitions}


transition = api.model('Transition', {
    'uri': fields.Url,
    'destination_state': ObjectUrl('api_v1.state', attribute='destination_state_id'),
    'source_state': ObjectUrl('api_v1.state', attribute='source_state_id'),
    'conditions': fields.List(fields.String)
})


@api.route('/transitions/<int:id>', endpoint='transition')
class TransitionAPI(Resource):
    @http_auth_required
    @api.marshal_with(transition)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified transition')
    def get(self, id: int):
        transition = models.Transition.query.filter(models.Transition.id == id).one_or_none()
        if transition is None:
            abort(404)
        return transition


# User API
user_list_get = api.model("UserListGet", {
    'users': fields.List(ObjectUrl('api_v1.user', attribute='id'))
})


user_get = api.model("UserGet", {
    'username': fields.String,
    'uri': fields.Url('api_v1.user'),
    'name': fields.String,
    'active': fields.Boolean,
    'email': fields.String,
    'create_time': fields.DateTime,
})


user_put = api.model("UserPut", {
    'username': fields.String,
    'name': fields.String,
    'active': fields.Boolean,
    'email': fields.String,
    'password': fields.String,
})


@api.route('/users', endpoint='users')
class UserListAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', type=str, required=True, location='json')
    request_parser.add_argument('password', type=str, required=True, location='json')
    request_parser.add_argument('name', type=str, required=True, location='json')
    request_parser.add_argument('email', type=str, required=True, location='json')
    request_parser.add_argument('active', type=bool, required=False, default=True, location='json')

    @http_auth_required
    @permissions_accepted('user_read_all')
    @api.marshal_with(user_list_get)
    @api.response(200, "Success")
    def get(self):
        users = models.User.query.all()
        return {'users': users}

    @http_auth_required
    @permissions_accepted('user_add')
    @api.marshal_with(user_get)
    @api.expect(user_put)
    @api.response(201, "Created user")
    def post(self):
        args = self.request_parser.parse_args()
        args['password'] = hash_password(args['password'])
        user = user_datastore.create_user(**args)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user, 201


@api.route('/users/<id>', endpoint='user')
class UserAPI(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('username', type=str, required=False, location='json')
    request_parser.add_argument('password', type=str, required=False, location='json')
    request_parser.add_argument('name', type=str, required=False, location='json')
    request_parser.add_argument('email', type=str, required=False, location='json')
    request_parser.add_argument('active', type=bool, required=False, location='json')

    @http_auth_required
    @permissions_accepted('user_read', 'user_read_all')
    @api.marshal_with(user_get)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to get this information")
    @api.response(404, "Could not find user")
    def get(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()

        if not has_permission_any('user_read_all'):
            if user != current_user:
                abort(403, "You are not authorized to get this information")

        if user is None:
            abort(404)

        return user

    @http_auth_required
    @permissions_accepted('user_update_all')
    @api.marshal_with(user_get)
    @api.expect(user_put)
    @api.response(200, "Success")
    @api.response(403, "You are not authorized to perform this operation")
    @api.response(404, "Could not find user")
    def put(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()
        if user is None:
            abort(404)

        args = self.request_parser.parse_args()

        if args['username'] is not None:
            user.username = args['username']

        if args['password'] is not None:
            user.password = args['password']

        if args['name'] is not None:
            user.name = args['name']

        if args['active'] is not None:
            user.active = args['active']

        if args['email'] is not None:
            user.email = args['email']

        db.session.commit()
        db.session.refresh(user)

        return user

    @http_auth_required
    @permissions_accepted('user_delete')
    @api.response(200, "Success")
    @api.response(404, "Could not find user")
    def delete(self, id):
        user = models.User.query.filter(models.User.id == id).one_or_none()

        if user is None:
            abort(404)

        user.active = False
        db.session.commit()


role_get = api.model("RoleGet", {
    'name': fields.String,
    'description': fields.String,
    'update_datetime': fields.DateTime,
    'permissions': fields.List(fields.String)
})


role_list_get = api.model("RoleListGet", {
    'roles': fields.List(ObjectUrl('api_v1.role', attribute='id'))
})


@api.route('/roles', endpoint='roles')
class RoleListAPI(Resource):
    @http_auth_required
    @permissions_accepted('roles_manage')
    @api.marshal_with(role_list_get)
    @api.response(200, "Success")
    def get(self):
        roles = models.Role.query.all()
        return {"roles": roles}


@api.route('/roles/<id>', endpoint='role')
class RoleApi(Resource):
    @http_auth_required
    @permissions_accepted('roles_manage')
    @api.marshal_with(role_get)
    @api.response(200, "Success")
    @api.response(404, "Could not find role")
    def get(self, id):
        role = models.Role.query.filter_by(id=id).one_or_none()
        if role is None:
            abort(404)
        return {'name': role.name,
                'description': role.description,
                'update_datetime': role.update_datetime,
                'permissions': role.get_permissions()}


@api.route('/users/<user_id>/roles/<role_id>', endpoint='userrole')
class UserRoleAPI(Resource):
    @auth_required('session', 'basic')
    @permissions_accepted('roles_manage')
    @api.response(200, "Success")
    @api.response(404, "User or Role not found")
    def put(self, user_id, role_id):
        role = get_object_from_arg(role_id, models.Role, models.Role.name)
        user = get_object_from_arg(user_id, models.User, models.User.username)

        if user not in role.users:
            role.users.append(user)
            db.session.commit()
            db.session.refresh(role)

        return {"role": role.id, "user": user.id, "has_role": user in role.users}

    @auth_required('session', 'basic')
    @permissions_accepted('roles_manage')
    @api.response(200, "Success")
    @api.response(404, "User or Role not found")
    def delete(self, user_id, role_id):
        role = get_object_from_arg(role_id, models.Role, models.Role.name)
        user = get_object_from_arg(user_id, models.User, models.User.username)

        user.roles = [x for x in user.roles if x != role]
        db.session.commit()
        db.session.refresh(user)
        db.session.refresh(role)

        return {"role": role.id, "user": user.id, "has_role": user in role.users}


workflow_list = api.model('WorkflowList', {
    'workflows': fields.List(ObjectUrl('api_v1.workflow', attribute='id'))
})


@api.route('/workflows', endpoint='workflows')
class WorkflowListAPI(Resource):
    @http_auth_required
    @api.marshal_with(workflow_list)
    @api.response(200, 'Success')
    def get(self):
        workflows = models.Workflow.query.all()
        return {'workflows': workflows}


workflow_model = api.model('Workflow', {
    'uri': fields.Url,
    'label': fields.String,
})


@api.route('/workflows/<id>', endpoint='workflow')
class WorkflowAPI(Resource):
    @http_auth_required
    @api.marshal_with(workflow_model)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified workflow')
    def get(self, id=None):
        workflow = get_object_from_arg(id, models.Workflow, models.Workflow.label)
        return workflow


@api.route('/workflows/<workflow_id>/states', endpoint='workflow_states')
class WorkflowStateListAPI(Resource):
    @http_auth_required
    @api.marshal_with(state_list)
    @api.response(200, 'Success')
    def get(self, workflow_id=None):
        workflow = get_object_from_arg(workflow_id, models.Workflow, models.Workflow.label)
        return {'states': workflow.states}


@api.route('/workflows/<workflow_id>/states/<state_id>', endpoint='workflow_state')
class WorkflowStateAPI(Resource):
    @http_auth_required
    @api.marshal_with(state_model)
    @api.response(200, 'Success')
    @api.response(404, 'Could not find specified state')
    def get(self, workflow_id=None, state_id=None):
        workflow = get_object_from_arg(workflow_id, models.Workflow, models.Workflow.label)
        state = get_object_from_arg(state_id, models.State, models.State.label, filters={models.State.workflow == workflow})
        return state
