# -*- coding: utf-8 -*-

from ..core import Service
from .models import Action


class ActionService(Service):
    __model__ = Action
