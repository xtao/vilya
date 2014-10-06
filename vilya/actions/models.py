# -*- coding: utf-8 -*-

from datetime import datetime
from ..core import db
from ..libs.const import ACTION_TYPES


class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.Integer(), default=ACTION_TYPES['comment'])
    type_id = db.Column(db.Integer())
    issue_id = db.Column(db.Integer())
    creator_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
