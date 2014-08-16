# -*- coding: utf-8 -*-

from ..core import Service
from .models import PullRequest


class PullRequestService(Service):
    __model__ = PullRequest
