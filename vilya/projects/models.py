# -*- coding: utf-8 -*-

from ..core import db
from .repository import ProjectRepository
from sqlalchemy import event


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
    def owner(self):
        from ..services import users
        return users.get(id=self.owner_id)

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

    def create_pullrequest(self, **kwargs):
        from ..services import pullrequests
        pr_kwargs = {}
        issue_kwargs = {}

        # new pr
        pr = pullrequests.create(**pr_kwargs)

        # new issue
        issue = self.create_issue(**issue_kwargs)

        # update pr
        pullrequests.update(pr, issue_id=issue.id)

        return pr

    def after_create_pullrequest(self, pr):
        pr.repo.sync()

    @property
    def next_issue_counter(self):
        self.issue_counter = Project.issue_counter + 1
        db.session.add(self)
        db.session.commit()
        return self.issue_counter

    @property
    def repository(self):
        return ProjectRepository(self)

    @property
    def path(self):
        return '%s.git' % self.id

    @property
    def remote_name(self):
        return str(self.id)

    def create_repository(self):
        # TODO git hook
        return ProjectRepository.init(self.path)


def after_create(mapper, connection, self):
    self.create_repository()


event.listen(Project, 'after_insert', after_create)
