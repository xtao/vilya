# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask.ext.login import current_user
from ..services import projects
from . import route

bp = Blueprint('vilya', __name__)


@route(bp, '/')
def index():
    context = {}
    if current_user.is_authenticated():
        context['projects'] = projects.find(owner_id=current_user.id)
        return render_template('people/dashboard.html', **context)
    return render_template('dashboard.html')
