# -*- coding: utf-8 -*-

from flask import (Blueprint,
                   g,
                   render_template,
                   flash,
                   redirect,
                   url_for,
                   abort,
                   request,
                   jsonify)
from flask.ext.login import current_user
from ..services import projects, users, issues
from ..forms import NewIssueForm, NewCommentForm
from ..libs.const import ISSUE_TYPES
from . import route

bp = Blueprint('issue', __name__, url_prefix='/<u_name>/<p_name>/issues')


@bp.url_value_preprocessor
def pull_project_code(endpoint, values):
    u_name = values.pop('u_name')
    p_name = values.pop('p_name')
    user = users.first(name=u_name)
    if not user:
        abort(404)
    project = projects.first(name=p_name, owner_id=user.id)
    if not project:
        abort(404)
    g.u_name = u_name
    g.p_name = p_name
    g.project = project


@route(bp, '/')
def index():
    context = {}
    context['u_name'] = g.u_name
    context['p_name'] = g.p_name
    context['project'] = g.project
    context['project_menu'] = 'Issues'
    project = g.project
    context['issues'] = issues.find(project_id=project.id, type=ISSUE_TYPES['default'])
    return render_template('issues/index.html', **context)


@route(bp, '/new')
def new():
    context = {}
    context['form'] = NewIssueForm()
    context['project'] = g.project
    context['project_menu'] = 'Issues'
    return render_template('issues/new.html', **context)


@route(bp, '/create', methods=['post'])
def create():
    context = {}
    context['u_name'] = g.u_name
    context['p_name'] = g.p_name
    context['project_menu'] = 'Issues'
    project = g.project
    form = NewIssueForm()
    if form.validate_on_submit():
        i = project.create_issue(creator_id=current_user.id,
                                 **form.data)
        flash('New issue was successfully created!', 'info')
        return redirect(url_for('.index', **context))
    context['form'] = form
    context['project'] = project
    return render_template('issues/new.html', **context)


@route(bp, '/<id>')
def issue(id):
    context = {}
    context['u_name'] = g.u_name
    context['p_name'] = g.p_name
    context['project'] = g.project
    context['project_menu'] = 'Issues'
    issue = issues.first(project_id=g.project.id,
                         number=id,
                         type=ISSUE_TYPES['default'])
    context['issue'] = issue
    context['new_comment_form'] = NewCommentForm()
    context['actions'] = issue.actions
    return render_template('issues/issue.html', **context)


@route(bp, '/<id>/comments', methods=['post'])
def issue_comment_index(id):
    # TODO move to api
    context = {}
    context['u_name'] = g.u_name
    context['p_name'] = g.p_name
    issue = issues.first(project_id=g.project.id,
                         number=id,
                         type=ISSUE_TYPES['default'])
    if request.method == 'POST':
        form = NewCommentForm()
        if form.validate_on_submit():
            comment = issue.create_comment(creator=current_user, **form.data)
            return redirect(url_for('.issue', id=id, **context))
            # return jsonify(comment=comment)
    return redirect(url_for('.issue', id=id, **context))
