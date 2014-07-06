# -*- coding: utf-8 -*-

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
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    closed_at = db.Column(db.DateTime())
