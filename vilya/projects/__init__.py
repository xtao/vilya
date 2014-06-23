# -*- coding: utf-8 -*-

from ..core import Service
from .models import Project


class ProjectService(Service):
    __model__ = Project
