# -*- coding: utf-8 -*-

from flask.ext.script import Command, prompt

from ..services import projects, users


class CreateProjectCommand(Command):
    """Create a project"""

    def run(self):
        # TODO not tested.
        name = prompt('Name')
        owner_name = prompt('OwnerName')
        user = users.first(name=owner_name)
        if not user:
            print 'Invalid user'
            return
        data = dict(name=name,
                    owner_id=user.id)
        project = projects.create(**data)
        if project:
            print '\nProject created successfully'
            print 'Project(id=%s name=%s owner=%s)' % (project.id, project.name, user.name)
            return
        print '\nError creating project'


class DeleteProjectCommand(Command):
    """Delete a project"""

    def run(self):
        repo_name = prompt('RepoName')
        user_name, project_name = repo_name.split('/')
        user = users.first(name=user_name)
        if not user:
            print 'Invalid user'
            return
        project = projects.first(name=project_name, owner_id=user.id)
        if not project:
            print 'Invalid project'
            return
        projects.delete(project)
        print 'Project deleted successfully'


class ListProjectsCommand(Command):
    """List all projects"""

    def run(self):
        for p in projects.all():
            if p.owner_id:
                user = p.owner
                name = user.name if user else p.owner_id
            else:
                name = p.owner_id
            print 'Project(id=%s name=%s owner=%s)' % (p.id, p.name, name)
