# -*- coding: utf-8 -*-

from ..core import Service
from .models import Project


class ProjectsService(Service):
    __model__ = Project

    def get_by_name_path(self, name_path):
        from ..services import users
        name_path = name_path[:-4]
        user_name, _, project_name = name_path.partition("/")
        user = users.first(name=user_name)
        if not user:
            return None
        project = self.first(owner_id=user.id, name=project_name)
        if not project:
            return None
        return project

    def fork(self, **kw):
        return self.create(**kw)
