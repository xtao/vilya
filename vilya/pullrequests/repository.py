# -*- coding: utf-8 -*-

from ..libs.git import PULL_REF_H, PULL_REF_M


class RepositoryMixin(object):

    def __init__(self, pullrequest):
        self.pullrequest = pullrequest
        self.origin_project = pullrequest.origin_project
        self.upstream_project = pullrequest.upstream_project

    @property
    def pull_origin_reference(self):
        return PULL_REF_H % self.pullrequest.number

    @property
    def pull_upstream_reference(self):
        return PULL_REF_M % self.pullrequest.number

    @property
    def origin_head_reference(self):
        if self.pullrequest.is_local():
            return 'refs/heads/%s' % self.origin_project_ref
        return 'refs/remotes/%s/%s' % (self.origin_project.remote_name,
                                       self.pullrequest.origin_project_ref)

    @property
    def upstream_head_reference(self):
        return 'refs/heads/%s' % self.pullrequest.upstream_project_ref


    def sync_reference(self):
        project = self.upstream_project
        project.repo.update_reference(self.pull_upstream_reference,
                                      self.upstream_head_reference)
        project.repo.update_reference(self.pull_origin_reference,
                                      self.origin_head_reference)

    def fetch(self):
        if self.pullrequest.is_local():
            return

        upstream = self.upstream_project
        origin = self.origin_project
        remotes = upstream.repo.remotes
        rs = [r.name for r in remotes]
        if origin.remote_name not in rs:
            upstream.repo.create_remote(origin.remote_name,
                                     origin.repo_path)
        upstream.repo.fetch(origin.remote_name)

    def sync(self):
        self.fetch()
        self.sync_reference()

    def merge(self):
        pass
