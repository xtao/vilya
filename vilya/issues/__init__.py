# -*- coding: utf-8 -*-

from ..core import Service
from .models import Issue


class IssuesService(Service):
    __model__ = Issue
