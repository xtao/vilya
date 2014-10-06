# -*- coding: utf-8 -*-

from ..core import Service
from .models import Comment


class CommentService(Service):
    __model__ = Comment
