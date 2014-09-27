# -*- coding: utf-8 -*-

from werkzeug.utils import cached_property


class Diff(object):

    def __init__(self, diff):
        self.diff = diff

    def __len__(self):
        return len(self.diff)

    def __iter__(self):
        for p in self.diff:
            yield Patch(p)

    @cached_property
    def additions(self):
        additions = 0
        for p in self.patches:
            additions += p.additions
        return additions

    @cached_property
    def deletions(self):
        deletions = 0
        for p in self.patches:
            deletions += p.deletions
        return deletions

    @property
    def patches(self):
        for p in self.diff:
            yield Patch(p)

    @property
    def deltas(self):
        return iter(self.diff)


class Patch(object):

    def __init__(self, patch):
        self.patch = patch

    @property
    def hunks(self):
        for h in self.patch.hunks:
            yield Hunk(h)


class Hunk(object):

    def __init__(self, hunk):
        self.hunk = hunk

    @property
    def lines(self):
        old = self.hunk.old_start
        new = self.hunk.new_start
        for a, l in self.hunk.lines:
            if a == '+':
                yield Line(a, l, old, 0)
                old += 1
            elif a == '-':
                yield Line(a, l, 0, new)
                new += 1
            elif a == '<':
                yield Line(a, l.lstrip('\n'), 0, 0)
            elif a == '>':
                yield Line(a, l.lstrip('\n'), 0, 0)
            else:
                yield Line(a, l, old, new)
                old += 1
                new += 1

    @property
    def heading(self):
        text = '@@ -%s,%s +%s,%s @@' % (self.hunk.old_start,
                                        self.hunk.old_lines,
                                        self.hunk.new_start,
                                        self.hunk.new_lines)
        old = 0
        new = 0
        attr = ''
        return Line(attr, text, old, new)


class Line(object):

    def __init__(self, attr, text, old, new):
        self.attr = attr
        self.text = text
        self.old = old
        self.new = new

    @property
    def old_num(self):
        return self.old if self.old else ''

    @property
    def new_num(self):
        return self.new if self.new else ''
