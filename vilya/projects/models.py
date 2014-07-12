# -*- coding: utf-8 -*-

from ..core import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(1024))
    upstream_id = db.Column(db.Integer)
    family_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    issue_counter = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    @property
    def full_name(self):
        from ..services import users
        u = users.get(id=self.owner_id)
        return '%s/%s' % (u.name, self.name)

    # TODO: transaction
    def create_issue(self, **kwargs):
        from ..services import issues

        # new issue
        issue = issues.create(**kwargs)

        # get new counter
        number = self.next_issue_counter

        # update issue
        issues.update(issue, project_id=self.id, number=number)
        return issue

    @property
    def next_issue_counter(self):
        self.issue_counter = Project.issue_counter + 1
        db.session.add(self)
        db.session.commit()
        return self.issue_counter
