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
        pull = pullrequests.create_pullrequest(project=self, **kwargs)
        pull.after_create()
        return pull

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

    def fork_repository(self, project):
        return project.repository.fork(self.path)

    @property
    def upstream(self):
        from ..services import projects
        return projects.get(id=self.upstream_id)


def after_create(mapper, connection, self):
    if self.upstream_id:
        self.fork_repository(self.upstream)
    else:
        self.create_repository()


event.listen(Project, 'after_insert', after_create)
