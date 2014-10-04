# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import FixedOffset
from ..libs.avatar import get_gravatar_url


class Commit(object):

    def __init__(self, commit):
        self.commit = commit

    @property
    def author(self):
        from ..services import users
        email = self.commit.author.email
        user = users.first(email=email)
        if not user:
            return None
        return user

    @property
    def author_time(self):
        return datetime.fromtimestamp(self.commit.author.time,
                                      FixedOffset(self.commit.author.offset))

    @property
    def author_name(self):
        author = self.author
        if not author:
            return self.commit.author.name
        if not author.name:
            return self.commit.author.name
        return author.name

    @property
    def author_url(self):
        author = self.author
        if not author:
            return None
        return author.url

    @property
    def author_avatar_url(self):
        author = self.author
        if not author:
            return get_gravatar_url(self.commit.author.email)
        return author.avatar_url

    @property
    def hex(self):
        return self.commit.hex

    @property
    def parents(self):
        return [Commit(p) for p in self.commit.parents]

    @property
    def message(self):
        return self.commit.message

    @property
    def message_title(self):
        title, _, _ = self.message.strip().partition('\n\n')
        return title

    @property
    def message_content(self):
        _, _, content = self.message.strip().partition('\n\n')
        return content
