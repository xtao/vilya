# -*- coding: utf-8 -*-

from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import current_user
from ..services import projects, users
from ..forms import NewProjectForm
from . import route

bp = Blueprint('project', __name__)


@route(bp, '/new')
def new():
    context = {}
    context['form'] = NewProjectForm()
    return render_template('projects/new.html', **context)


@route(bp, '/create', methods=['POST'])
def create():
    """Create a new course."""
    form = NewProjectForm()
    if form.validate_on_submit():
        p = projects.create(owner_id=current_user.id, **form.data)
        flash('New course was successfully created!', 'info')
        return redirect(url_for('.index',
                                u_name=current_user.name,
                                p_name=p.name))
    return render_template('projects/new.html', form=form)


@route(bp, '/<u_name>/<p_name>')
def index(u_name, p_name):
    context = {}
    p_user = users.first(name=u_name)
    context['project'] = projects.first(name=p_name, owner_id=p_user.id)
    return render_template('projects/index.html', **context)
