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

import datetime
from . import conditions
from . import exceptions
from .callbacks import dispatch_callback
from flask import url_for, current_app
from sqlalchemy import and_, func
from flask_sqlalchemy import SQLAlchemy

from .auth.models import BaseUser
from .auth.models import BaseRole

# Get the database
db = SQLAlchemy()


class Workflow(db.Model):
    __tablename__ = 'workflow'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), unique=True, nullable=False)

    states = db.relationship("State", backref="workflow")


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.DATE, nullable=False)

    experiments = db.relationship("Experiment", backref="subject")
    external_subject_links = db.relationship("ExternalSubjectLinks", backref="subject")

    def __init__(self, label=None, date_of_birth=None):
        self.label = label
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return "<Subject label={}, id={}, dob={}>".format(self.label, self.id, self.date_of_birth)

    @property
    def external_ids(self):
        return {x.external_system.system_name: x.external_id for x in self.external_subject_links}


class ExternalSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.VARCHAR(100), unique=True)
    url = db.Column(db.VARCHAR(512))

    external_subject_links = db.relationship("ExternalSubjectLinks", backref="external_system")
    external_experiment_links = db.relationship("ExternalExperimentLinks", backref="external_system")

    def __init__(self, id=None, system_name=None, url=None):
        if id is not None:
            self.id = id

        self.system_name = system_name
        self.url = url

    def __repr__(self):
        return "<ExternalSystem {} (id={})>".format(self.system_name, self.id)


class ExternalSubjectLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(1024))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', name='fk_external_subject_links_subject_id_subject'))
    external_system_id = db.Column(db.Integer, db.ForeignKey('external_system.id', name='fk_external_subject_links_external_system_id_external_system'))

    # Make sure every link can only exist once (one external id per combination of experiment and system)
    unique_constraint = db.UniqueConstraint('subject_id', 'external_system_id', name='uix_subject_id_external_system_id')

    def __init__(self, external_id=None, subject=None, external_system=None):
        self.external_id = external_id
        self.subject = subject
        self.external_system = external_system

    def __repr__(self):
        return "<ExternalSubjectLink subject={}, external_id={}, external_system={}>".format(self.subject, self.external_id, self.external_system)


class ExternalExperimentLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(1024))

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_external_experiment_links_experiment_id_experiment'))
    external_system_id = db.Column(db.Integer, db.ForeignKey('external_system.id', name='fk_external_experiment_links_external_system_id_external_system'))

    # Make sure every link can only exist once (one external id per combination of experiment and system)
    unique_constraint = db.UniqueConstraint('experiment_id', 'external_system_id', name='uix_experiment_id_external_system_id')

    def __init__(self, external_id=None, experiment=None, external_system=None):
        self.external_id = external_id
        self.experiment = experiment
        self.external_system = external_system

    def __repr__(self):
        return "<ExternalExperimentLink experiment={}, external_id={}, external_system={}>".format(self.experiment, self.external_id, self.external_system)


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_scan_experiment_id_experiment'))
    scantype_id = db.Column(db.Integer, db.ForeignKey('scantype.id', name='fk_scan_scantype_id_scantype'))

    def __init__(self, experiment=None, scantype=None):
        self.experiment = experiment
        self.scantype = scantype

    def __repr__(self):
        return "<Scan experiment={}, scantype={}>".format(self.experiment, self.scantype)


class Scantype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modality = db.Column(db.VARCHAR(100), nullable=False)
    protocol = db.Column(db.VARCHAR(100), nullable=False, unique=True)

    scans = db.relationship("Scan", backref='scantype')

    def __init__(self, id=None, modality=None, protocol=None):
        if id is not None:
            self.id = id

        self.modality = modality
        self.protocol = protocol

    def __repr__(self):
        return "<Scantype modality={}, protocol={}, id={}>".format(self.modality, self.protocol, self.id)


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    scandate = db.Column(db.DATETIME, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', name='fk_experiment_subject_id_subject'))

    scans = db.relationship("Scan", cascade="all, delete-orphan", backref='experiment')
    actions = db.relationship("Action", cascade="all, delete-orphan", backref='experiment')
    external_experiment_links = db.relationship("ExternalExperimentLinks",
                                                cascade="all, delete-orphan",
                                                backref="experiment"
                                                )

    @property
    def state(self):
        action = Action.query.filter(Action.experiment == self).order_by(Action.start_time.desc(), Action.id.desc()).first()

        if action is None:
            return None

        return action.transition.destination_state

    @state.setter
    def state(self, target_state):
        self.set_state(target_state)

    def set_state(self, target_state, api_prefix='api_v1', freetext=None):
        transition = self.state.get_transition_to(target_state)
        print('Desired transition: {}'.format(transition))

        if transition is None:
            raise exceptions.NoValidTransitionError(self.state, target_state)

        if freetext is None:
            freetext = "Transition triggered by setting state to {} ({})".format(
                target_state.label,
                target_state.id,
            )

        self._set_state(transition, api_prefix=api_prefix, freetext=freetext)

    def _set_state(self, transition, api_prefix='api_v1', freetext=None):
        for condition in transition.conditions:
            result = condition.check(self)
            if not result:
                raise exceptions.ConditionNotMetError(experiment=self, transition=transition, condition=condition)

        # Do the actual transition by creating an Action
        current_app.logger.error('[INFO] Adding action')

        action = Action(experiment=self,
                        transition=transition,
                        freetext=freetext)

        print('Adding action: {}'.format(action))
        current_app.logger.error('Adding action: {}'.format(action))
        db.session.add(action)
        db.session.commit()
        print('Committed')
        current_app.logger.error('Committed')

        # Dispatch the callback, or set to done if there is no callback
        if transition.destination_state.callback:
            current_app.logger.error('Dispatching callback')
            dispatch_callback(transition.destination_state.callback,
                              url_for('{}.action'.format(api_prefix), id=action.id, _external=True),
                              current_app.config)
            current_app.logger.error('Dispatching done')

        else:
            action.success = True
            action.end_time = datetime.datetime.now()
            action.return_value = 'No callback for state'

    @property
    def external_ids(self):
        return {x.external_system.system_name: x.external_id for x in self.external_experiment_links}

    def find_external_id(self, external_system_name):
        result = tuple(x for x in self.external_experiment_links if x.external_system.system_name == external_system_name)
        if len(result) != 1:
            raise ValueError("Found multiple links to external system")

        return result[0].external_system_id

    def __init__(self, workflow, subject=None, label=None, scandate=None):
        self.subject = subject
        self.label = label
        self.scandate = scandate

        # Find the one state in the workflow that has no incoming transitions
        root_state = State.query.filter(State.workflow == workflow).filter(~State.transition_destinations.any()).one()
        initial_transition = Transition.query.filter(Transition.source_state == root_state).one()
        self._set_state(initial_transition)

    def __repr__(self):
        return "<Experiment label={}, id={}, subject={}, scandate={}>".format(self.label, self.id, self.subject_id, self.scandate)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    success = db.Column(db.Boolean, nullable=False)
    return_value = db.Column(db.Text)
    freetext = db.Column(db.Text)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)

    transition_id = db.Column(db.Integer, db.ForeignKey('transition.id', name='fk_action_transition_id_transition'))
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_action_experiment_id_experiment'))

    def __init__(self, experiment=None, transition=None, freetext=None):
        self.experiment = experiment
        self.transition = transition
        self.freetext = freetext
        self.success = False
        self.start_time = datetime.datetime.now()

    def __repr__(self):
        return "<Action transition={}, id={}, experiment={}, start_time={}>".format(self.transition, self.id, self.experiment, self.start_time)


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), nullable=False)
    callback = db.Column(db.Text)
    # Store the lifespan in seconds as an Integer
    lifespan = db.Column(db.Integer)
    freetext = db.Column(db.Text)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id', name='fk_state_workflow_id_workflow'))

    # Make sure the combination of label and workflow id stays unique
    unique_constraint = db.UniqueConstraint('label', 'workflow_id', name='uix_label_workflow_id')

    transition_sources = db.relationship("Transition",
                                         foreign_keys='Transition.source_state_id',
                                         backref="source_state"
                                         )
    transition_destinations = db.relationship("Transition",
                                              foreign_keys='Transition.destination_state_id',
                                              backref="destination_state"
                                              )

    @property
    def lifespan_timedelta(self):
        return datetime.timedelta(seconds=self.lifespan)

    def __init__(self, id=None, label=None, callback=None, lifespan=None, freetext=None, workflow=None):
        if id is not None:
            self.id = id
        self.label = label
        self.callback = callback
        self.lifespan = lifespan
        self.freetext = freetext
        self.workflow = workflow

    def __repr__(self):
        return "<State state={}, id = {}, lifespan = {}>".format(self.label, self.id, self.lifespan)

    @property
    def experiments(self):
        # Find last start_time of actions related to a single experiment
        last_times = db.session.query(Action.experiment_id, func.max(Action.start_time).label('last_time')).group_by(Action.experiment_id).subquery()

        # Find last id in case start_times are duplicated
        last_actions = db.session.query(Action.experiment_id, func.max(Action.id).label('latest_action_ids'), Action.start_time).join((last_times, and_(Action.experiment_id == last_times.c.experiment_id, Action.start_time == last_times.c.last_time))).group_by(Action.experiment_id).subquery()

        # Join Experiment all the way to State
        return db.session.query(Experiment).join(Action).join((last_actions, Action.id == last_actions.c.latest_action_ids)).join(Transition).join(State, Transition.destination_state_id == State.id).filter(State.id == self.id).all()

    def get_transition_to(self, target_state):
        return Transition.query.filter(Transition.source_state == self,
                                       Transition.destination_state == target_state).one_or_none()


# Definition of the association table between transtions and conditions.
transition_has_condition_table = db.Table('transition_has_condition', db.metadata,
                                          db.Column('transition_id',
                                                    db.Integer,
                                                    db.ForeignKey('transition.id', name='fk_transition_has_condition_transition_id_transition')),
                                          db.Column('condition_id',
                                                    db.Integer,
                                                    db.ForeignKey('condition.id', name='fk_transition_has_condition_condition_id_condition')))


class Transition(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    source_state_id = db.Column(db.Integer, db.ForeignKey('state.id', name='fk_transition_source_state_id_state'))
    destination_state_id = db.Column(db.Integer, db.ForeignKey('state.id', name='fk_transition_destination_state_id_state'))

    actions = db.relationship("Action", backref="transition")
    conditions = db.relationship("Condition", secondary=transition_has_condition_table, backref="transitions")

    def __init__(self, id=None, source_state=None, destination_state=None, conditions=None):
        if id is not None:
            self.id = id

        if conditions is None:
            conditions = []

        self.source_state = source_state
        self.destination_state = destination_state
        self.conditions = conditions

    def __repr__(self):
        return "<Transition: source={} -> destination={}, conditions={}, id={}>".format(self.source_state, self.destination_state, self.conditions, self.id)


class Condition(db.Model):
    __tablename__ = "condition"

    id = db.Column(db.Integer, primary_key=True)
    rule = db.Column(db.VARCHAR(500), nullable=False)
    freetext = db.Column(db.Text)

    def __init__(self, rule=None, freetext=None):
        self.rule = rule
        self.freetext = freetext

    def __repr__(self):
        return "<Condition rule = {}, id = {}>".format(self.rule, self.id)

    def check(self, experiment):
        return conditions.master_condition(experiment=experiment, data=self.rule, condition_id=self.id)


# User and Role models used for authentication and authorization
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id', name="fk_roles_users_user_id_user")),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', name="fk_roles_users_role_id_role"))
                       )


class Role(db.Model, BaseRole):
    """ This implements the BaseRole from the .auth.models module.
    In this specific case, the BaseRole is sufficient. """
    __tablename__ = 'role'
    pass


class User(db.Model, BaseUser):
    __tablename__ = 'user'
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username} ({self.name})>'
