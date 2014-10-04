# -*- coding: utf-8 -*-

import os
import shutil
from ..libs.git import PULL_REF_H, PULL_REF_M, make_git_env
from ..settings import TEMP_PATH


class PushError(Exception):
    pass


class MergeError(Exception):
    pass


class Repository(object):

    def __init__(self, pullrequest):
        self.pullrequest = pullrequest
        self.origin_project = pullrequest.origin_project
        self.upstream_project = pullrequest.upstream_project
        self.repository = self.upstream_project.repository
        self.origin_repository = self.origin_project.repository

    @property
    def pull_origin_reference(self):
        return PULL_REF_H % self.pullrequest.number

    @property
    def pull_upstream_reference(self):
        return PULL_REF_M % self.pullrequest.number

    @property
    def origin_head_reference(self):
        reference = self.pullrequest.origin_project_ref
        if self.pullrequest.is_local():
            return 'refs/heads/%s' % reference
        # TODO origin_remote_name
        return 'refs/remotes/%s/%s' % (self.origin_project.remote_name,
                                       reference)
    @property
    def cloned_origin_head_reference(self):
        reference = self.pullrequest.origin_project_ref
        if self.pullrequest.is_local():
            return 'origin/%s' % reference
        # TODO origin_remote_name
        return 'refs/remotes/%s/%s' % (self.origin_project.remote_name,
                                       reference)

    @property
    def upstream_head_reference(self):
        return 'refs/heads/%s' % self.pullrequest.upstream_project_ref

    def sync_pull_reference(self):
        repo = self.upstream_project.repository
        repo.update_reference(self.pull_upstream_reference,
                              self.upstream_head_reference)
        repo.update_reference(self.pull_origin_reference,
                              self.origin_head_reference)

    def fetch(self, repo=None):
        if self.pullrequest.is_local():
            return

        origin = self.origin_project
        if not repo:
            repo = self.repository

        remotes = repo.list_remotes()
        rs = [r.name for r in remotes]
        if origin.remote_name not in rs:
            repo.create_remote(origin.remote_name,
                               origin.repository.path)
        repo.fetch(origin.remote_name)

    def sync(self):
        self.fetch()
        self.sync_pull_reference()

    # TODO multi-line message
    def merge(self, merger, message):
        commit = None
        worktree = self.temp_path
        try:
            user = self.upstream_project.owner
            env = make_git_env(user.name, user.email)
            upstream_project_ref = self.pullrequest.upstream_project_ref
            repo = self.repository.clone(worktree, bare=False,
                                         branch=upstream_project_ref,
                                         shared=True)
            self.fetch(repo)
            reference = self.origin_head_reference
            errcode = repo.merge(reference,
                                 no_ff=True,
                                 m=message,
                                 env=env)
            if errcode != 0:
                raise MergeError
            # TODO CODE_REMOTE_USER
            errcode = repo.push('origin', upstream_project_ref)
            if errcode != 0:
                raise PushError
            commit = self.repository.resolve_commit(upstream_project_ref)
        except MergeError:
            pass
        except PushError:
            pass
        finally:
            shutil.rmtree(worktree)
        return commit

    @property
    def can_fastforward(self):
        commits = self.repository.list_commits(self.upstream_commit_hex,
                                               self.origin_commit_hex)
        if not commits:
            return True

    @property
    def can_merge(self):
        r = False
        worktree = self.temp_path
        try:
            user = self.upstream_project.owner
            env = make_git_env(user.name, user.email)
            repo = self.repository.clone_to(worktree, bare=False,
                                            branch=self.pullrequest.upstream_project_ref,
                                            shared=True)
            self.fetch(repo)
            reference = self.cloned_origin_head_reference
            repo.merge(reference,
                       no_ff=True,
                       m='automerge',
                       env=env)
            r = True
        finally:
            shutil.rmtree(worktree)
        return r

    @property
    def origin_commit_hex(self):
        hex = None
        try:
            reference = self.pull_origin_reference
            commit = self.repository.resolve_commit(reference)
            hex = commit.hex
        except:
            pass

        if hex:
            return hex
        repo = self.origin_repository
        if not repo:
            return hex

        try:
            reference = self.pullrequest.origin_project_ref
            commit = repo.resolve_commit(reference)
            hex = commit.hex
        except:
            pass

        return hex

    @property
    def upstream_commit_hex(self):
        hex = None
        try:
            reference = self.pull_upstream_reference
            commit = self.repository.resolve_commit(reference)
            hex = commit.hex
        except:
            pass

        if hex:
            return hex

        try:
            reference = self.pullrequest.upstream_project_ref
            commit = self.repository.resolve_commit(reference)
            hex = commit.hex
        except:
            pass

        return hex

    @property
    def merge_base_hex(self):
        upstream = self.upstream_commit_hex
        origin = self.origin_commit_hex
        commit = None
        if upstream and origin:
            commit = self.repository.resolve_merge_base(upstream, origin)
        if not commit:
            return upstream
        return commit.hex

    @property
    def temp_path(self):
        import tempfile
        if hasattr(self, "_temp_path"):
            return self._temp_path

        temp_pull_path = os.path.join(TEMP_PATH, "pull")
        if not os.path.exists(temp_pull_path):
            os.makedirs(temp_pull_path)
        worktree = tempfile.mkdtemp(dir=temp_pull_path)
        self._temp_path = worktree
        return worktree

    @property
    def commits(self):
        return self.repository.list_commits(self.origin_commit_hex,
                                            self.upstream_commit_hex)

    @property
    def files(self):
        return []

    @property
    def diff(self):
        return self.repository.diff(self.origin_commit_hex,
                                    self.merge_base_hex)
