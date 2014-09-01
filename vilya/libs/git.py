# -*- coding: utf-8 -*-

from ellen.repository import Repository as _Repository


class Repository(object):

    def __init__(self, path):
        self.path = path
        self.repository = _Repository(path)

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

    def list_commits(self, reference='HEAD', path=None, max_count=25):
        return self.repository.list_commits(reference,
                                            path=path,
                                            max_count=max_count)

    def resolve_commit(self, reference):
        return self.repository.resolve_commit(reference)

    def diff(self, reference, from_reference=None):
        return self.repository.diff(reference, from_reference=from_reference)
