# -*- coding: utf-8 -*-

from datetime import datetime
from ..core import db


class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    number = db.Column(db.Integer())
    project_id = db.Column(db.Integer())
    creator_id = db.Column(db.Integer())
    closer_id = db.Column(db.Integer())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = db.Column(db.DateTime())
