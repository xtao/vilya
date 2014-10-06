# -*- coding: utf-8 -*-

from .projects import ProjectsService
from .users import UsersService
from .issues import IssuesService
from .pullrequests import PullRequestService
from .comments import CommentService
from .actions import ActionService

projects = ProjectsService()
users = UsersService()
issues = IssuesService()
pullrequests = PullRequestService()
comments = CommentService()
actions = ActionService()
