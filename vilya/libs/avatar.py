# -*- coding: utf-8 -*-

import urllib
import hashlib

DEFAULT_USER = "http://img3.douban.com/icon/user_normal.jpg"


def get_gravatar_url(email, size=140):
    normalized_email = email.encode('utf8').lower()
    url = "https://secure.gravatar.com/avatar/%s?%s" % (
        hashlib.md5(normalized_email).hexdigest(),
        urllib.urlencode({'d': DEFAULT_USER,
                          's': str(size),
                          'r': 'x'}))
    return url
