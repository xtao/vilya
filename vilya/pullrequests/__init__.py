# -*- coding: utf-8 -*-

from ..core import Service
from .models import PullRequest


class PullRequestService(Service):
    __model__ = PullRequest

    def create_pullrequest(self, **kwargs):
        project = kwargs.get('project')

        pull_kwargs = self.get_pull_kwargs(**kwargs)

        issue_kwargs = dict(
            name=kwargs.get('name'),
            description=kwargs.get('description'),
            creator_id=kwargs.get('creator_id'),
        )

        # new pull
        pull = self.create(**pull_kwargs)

        # new issue
        issue = project.create_issue(**issue_kwargs)

        # update pull
        self.update(pull, issue_id=issue.id)

        return pull

    def validate_pullrequest(self, **kwargs):
        return

    def new_pullrequest(self, **kwargs):
        pull_kwargs = self.get_pull_kwargs(**kwargs)
        # new pull
        pull = self.new(**pull_kwargs)
        return pull

    def get_pull_kwargs(self, **kwargs):
        from ..services import projects

        project = kwargs.get('project')
        origin = kwargs.get('origin')
        origin_project = project
        if not origin:
            origin_project_id = project.id
            origin_project_ref = 'master'
        else:
            repo_name, _, reference = origin.rpartition(':')
            if repo_name:
                origin_project = projects.get_by_repo_name(repo_name)
            origin_project_ref = reference
            origin_project_id = origin_project.id
        c = origin_project.repository.resolve_commit(origin_project_ref)
        origin_commit_sha = c.hex

        upstream = kwargs.get('upstream')
        upstream_project = project
        if not upstream:
            upstream_project_id = project.id
            upstream_project_ref = 'master'
        else:
            repo_name, _, reference = upstream.rpartition(':')
            if repo_name:
                upstream_project = projects.get_by_repo_name(repo_name)
            upstream_project_ref = reference
            upstream_project_id = upstream_project.id
        c = upstream_project.repository.resolve_commit(upstream_project_ref)
        upstream_commit_sha = c.hex

        pull_kwargs = dict(
            creator_id=kwargs.get('creator_id'),
            origin_project_id=origin_project_id,
            origin_project_ref=origin_project_ref,
            origin_commit_sha=origin_commit_sha,
            upstream_project_id=upstream_project_id,
            upstream_project_ref=upstream_project_ref,
            upstream_commit_sha=upstream_commit_sha,
        )
        return pull_kwargs
