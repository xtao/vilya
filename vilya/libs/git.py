# -*- coding: utf-8 -*-

from ellen.repository import Repository as _Repository
from .diff import Diff

PULL_REF_H = 'refs/pulls/%s/head'
PULL_REF_M = 'refs/pulls/%s/merge'


class Repository(object):

    def __init__(self, path):
        self.path = path
        self.repository = _Repository(path)

    @property
    def is_empty(self):
        return self.repository.is_empty

    @property
    def head(self):
        return self.repository.head

    def get_file(self, reference, path):
        blob = self.repository.resolve_blob("%s:%s" % (reference,
                                                       path))
        if not blob:
            return None
        return blob.data

    def list_entries(self, reference='HEAD', path=None):
        return self.repository.list_entries(reference,
                                            path=path)

    def list_branches(self):
        return self.repository.list_branches()

    def list_tags(self):
        return self.repository.list_tags()

    def list_commits(self, reference='HEAD', from_reference=None, path=None, max_count=25):
        return self.repository.list_commits(reference,
                                            from_ref=from_reference,
                                            path=path,
                                            max_count=max_count)

    def resolve_commit(self, reference):
        return self.repository.resolve_commit(reference)

    def diff(self, reference, from_reference=None):
        raw_diff = self.repository.diff(reference, from_reference=from_reference)
        if raw_diff:
            return Diff(raw_diff)
        return raw_diff

    def list_remotes(self):
        return self.repository.list_remotes()

    def create_remote(self, name, url):
        return self.repository.create_remote(name, url)

    @classmethod
    def clone(cls, *k, **kw):
        return _Repository.clone(*k, **kw)

    @classmethod
    def init(cls, path, bare=True):
        return _Repository.init(path, bare=bare)

    def merge(self, *k, **kw):
        return self.repository.merge(*k, **kw)

    def fetch(self, name=None):
        return self.repository.fetch(name)

    def resolve_merge_base(self, reference, from_reference):
        return self.repository.merge_base(reference, from_reference)

    def update_reference(self, *k):
        return self.repository.update_reference(*k)

    def resolve_type(self, reference):
        return self.repository.resolve_type(reference)

def make_git_env(user=None, is_anonymous=False):
    env = {}
    if is_anonymous:
        env['GIT_AUTHOR_NAME'] = 'anonymous'
        env['GIT_AUTHOR_EMAIL'] = 'anonymous@douban.com'
        env['GIT_COMMITTER_NAME'] = 'anonymous'
        env['GIT_COMMITTER_EMAIL'] = 'anonymous@douban.com'
    else:
        env['GIT_AUTHOR_NAME'] = user.name
        env['GIT_AUTHOR_EMAIL'] = user.email
        env['GIT_COMMITTER_NAME'] = user.name
        env['GIT_COMMITTER_EMAIL'] = user.email
    return env
