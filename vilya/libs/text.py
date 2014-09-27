# -*- coding: utf-8 -*-

import docutils
from mikoto import Mikoto

# FIXME new api
from mikoto.libs.text import RST_RE

def format_md_or_rst(path, content, project_name=None):
    m = Mikoto(content)
    if path.endswith('.md') or path.endswith('.markdown'):
        # FIXME with project or gist
        return m.markdown

    if RST_RE.match(path):
        try:
            return m.restructuredtext
        except docutils.ApplicationError:
            pass

    return m.highlight_code(path)
