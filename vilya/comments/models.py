# -*- coding: utf-8 -*-

from datetime import datetime
from ..core import db
from ..libs.const import COMMENT_TYPES


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer(), default=COMMENT_TYPES['issue'])
    description = db.Column(db.Text)
    issue_id = db.Column(db.Integer())
    creator_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def creator(self):
        from ..services import users
        if not self.creator_id:
            return None
        return users.get(id=self.creator_id)
