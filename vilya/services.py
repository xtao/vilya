# -*- coding: utf-8 -*-

from .projects import ProjectsService
from .users import UsersService
from .issues import IssuesService

projects = ProjectsService()
users = UsersService()
issues = IssuesService()
