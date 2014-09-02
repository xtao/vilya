# -*- coding: utf-8 -*-

from ..core import db


class PullRequest(db.Model):
    __tablename__ = 'pullrequests'

    id = db.Column(db.Integer(), primary_key=True)
    issue_id = db.Column(db.Integer())
    origin_project_id = db.Column(db.Integer())
    origin_project_ref = db.Column(db.String(1024))
    upstream_project_id = db.Column(db.Integer())
    upstream_project_ref = db.Column(db.String(1024))
    origin_commit_sha = db.Column(db.String(40))
    upstream_commit_sha = db.Column(db.String(40))
    merged_commit_sha = db.Column(db.String(40))
    merger_id = db.Column(db.Integer())
    creator_id = db.Column(db.Integer())
    merged_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())


    def is_local(self):
        return self.origin_project_id == self.upstream_project_id
