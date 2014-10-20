# -*- coding: utf-8 -*-

from datetime import datetime
from ..core import db
from ..libs.const import ISSUE_TYPES


class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    number = db.Column(db.Integer())
    type = db.Column(db.Integer(), default=ISSUE_TYPES['default'])
    project_id = db.Column(db.Integer())
    creator_id = db.Column(db.Integer())
    closer_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = db.Column(db.DateTime())

    @property
    def creator(self):
        from ..services import users
        if not self.creator_id:
            return None
        return users.get(id=self.creator_id)

    @property
    def closer(self):
        from ..services import users
        if not self.closer_id:
            return None
        return users.get(id=self.closer_id)

    @property
    def actions(self):
        from ..services import actions
        return actions.find(issue_id=self.id)

    def create_comment(self, description, creator):
        from ..services import actions, comments
        comment = comments.create(description=description,
                                  issue_id=self.id,
                                  creator_id=creator.id)
        action = actions.create(type_id=comment.id,
                                issue_id=self.id,
                                creator_id=creator.id)
        return comment

    def close_issue(self, closer):
        from ..services import issues
        self.closer_id = closer.id
        self.closed_at = datetime.utcnow()
        issues.save(self)
        # TODO action

    def reopen_issue(self, creator):
        from ..services import issues
        self.closer_id = None
        self.closed_at = None
        issues.save(self)
        # TODO action
