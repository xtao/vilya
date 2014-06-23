# -*- coding: utf-8 -*-

from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import current_user
from ..services import projects
from . import route

bp = Blueprint('people', __name__)

@route(bp, '/<u_name>')
def index(u_name):
    context = {}
    context['user'] = current_user
    context['projects'] = projects.find(owner_id=current_user.id)
    return render_template('people/index.html', **context)
