# -*- coding: utf-8 -*-

from ..core import Service
from .models import User


class UsersService(Service):
    __model__ = User

    def get_by_name_path(self, name_path):
        name_path = name_path[:-4]
        user_name, _, project_name = name_path.partition("/")
        user = self.first(name=user_name)
        if not user:
            return None
        return user
