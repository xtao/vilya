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
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    context['reference'] = project.repository.head.name
    context['path'] = None

    if project.repository.is_empty:
        context['project_menu'] = 'Code'
        return render_template('projects/empty.html', **context)

    generate_tree_context(context)
    return render_template('projects/tree.html', **context)


@route(bp, '/<u_name>/<p_name>/')
def index_301(u_name, p_name):
    return redirect(url_for('.index',
                            u_name=u_name,
                            p_name=p_name))


@route(bp, '/<u_name>/<p_name>/fork')
def fork(u_name, p_name):
    context = {}
    user = current_user
    p_user = users.first(name=u_name)
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    # find user project
    family_id = project.family_id if project.family_id else project.id
    fork_project = projects.first(family_id=family_id, owner_id=user.id)
    if fork_project:
        return redirect(url_for('.index',
                                u_name=user.name,
                                p_name=fork_project.name))
    # create project
    data = {}
    data['name'] = project.name
    data['description'] = project.description
    data['upstream_id'] = project.id
    if project.family_id:
        family_id = project.family_id
    elif project.upstream_id:
        family_id = project.upstream_id
    else:
        family_id = project.id
    data['family_id'] = family_id
    data['owner_id'] = user.id
    # fork project
    fork_project = projects.fork(**data)
    return redirect(url_for('.index',
                            u_name=user.name,
                            p_name=fork_project.name))


@bp.route('/<u_name>/<p_name>/tree/<reference>')
@bp.route('/<u_name>/<p_name>/tree/<reference>/<path:path>')
def tree_index(u_name, p_name, reference, path=None):
    context = {}
    p_user = users.first(name=u_name)
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    context['reference'] = reference
    context['path'] = path

    if project.repository.is_empty:
        context['project_menu'] = 'Code'
        return render_template('projects/empty.html', **context)

    generate_tree_context(context)
    return render_template('projects/tree.html', **context)


@route(bp, '/<u_name>/<p_name>/blob/<reference>/<path:path>')
def blob_index(u_name, p_name, reference, path):
    context = {}
    p_user = users.first(name=u_name)
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    context['reference'] = reference
    context['path'] = path

    if project.repository.is_empty:
        return redirect(url_for('.index',
                                u_name=u_name,
                                p_name=p_name))

    generate_blob_context(context)
    return render_template('projects/blob.html', **context)


@bp.route('/<u_name>/<p_name>/commits', defaults={'reference': 'HEAD', 'path': None})
@bp.route('/<u_name>/<p_name>/commits/<reference>', defaults={'path': None})
@bp.route('/<u_name>/<p_name>/commits/<reference>/<path:path>')
def commits_index(u_name, p_name, reference, path):
    context = {}
    p_user = users.first(name=u_name)
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    context['reference'] = reference
    context['path'] = path

    if project.repository.is_empty:
        return redirect(url_for('.index',
                                u_name=u_name,
                                p_name=p_name))

    generate_commits_context(context)
    return render_template('projects/commits.html', **context)


@route(bp, '/<u_name>/<p_name>/commit/<reference>')
def commit_index(u_name, p_name, reference):
    context = {}
    p_user = users.first(name=u_name)
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    context['reference'] = reference

    if project.repository.is_empty:
        return redirect(url_for('.index',
                                u_name=u_name,
                                p_name=p_name))

    generate_commit_context(context)
    return render_template('projects/commit.html', **context)


@bp.route('/<u_name>/<p_name>/compare')
@bp.route('/<u_name>/<p_name>/compare/<path:reference>')
def compare_index(u_name, p_name, reference=None):
    context = {}
    p_user = users.first(name=u_name)
    project = projects.first(name=p_name, owner_id=p_user.id)
    context['project'] = project
    context['reference'] = reference

    if project.repository.is_empty:
        return redirect(url_for('.index',
                                u_name=u_name,
                                p_name=p_name))

    generate_compare_context(context)
    return render_template('projects/compare.html', **context)


def generate_tree_context(context):
    project = context['project']
    reference = context['reference']
    path = context['path']
    repo = project.repository

    context['project_menu'] = 'Code'
    context['references'] = {'branches': repo.list_branches(),
                             'tags': repo.list_tags()}
    context['readme'] = repo.get_readme(reference=reference,
                                        path=path)
    context['entries'] = repo.list_entries(reference=reference,
                                           path=path)
    generate_base_context(context)
    return context


def generate_blob_context(context):
    project = context['project']
    reference = context['reference']
    path = context['path']

    context['project_menu'] = 'Code'
    context['references'] = {'branches': project.repository.list_branches(),
                             'tags': project.repository.list_tags()}
    context['file'] = project.repository.get_rendered_file(reference=reference,
                                                           path=path)
    generate_base_context(context)
    return context


def generate_commits_context(context):
    project = context['project']
    reference = context['reference']
    path = context['path']

    context['project_menu'] = 'Commits'
    context['references'] = {'branches': project.repository.list_branches(),
                             'tags': project.repository.list_tags()}
    context['commits'] = project.repository.list_commits(reference=reference,
                                                         path=path)
    generate_base_context(context)
    return context


def generate_commit_context(context):
    context['project_menu'] = 'Commits'
    project = context['project']
    reference = context['reference']

    commit = project.repository.resolve_commit(reference=reference)
    context['commit'] = commit
    context['diff'] = project.repository.diff(commit.hex)
    generate_base_context(context)
    return context


def generate_compare_context(context):
    from ..services import pullrequests
    kwargs = {}
    project = context['project']
    reference = context['reference']
    from_reference = reference
    to_reference = project.repository.head.name
    if '...' in reference:
        from_reference, _, to_reference = reference.partition('...')
    kwargs['upstream'] = from_reference
    kwargs['origin'] = to_reference
    kwargs['project'] = project
    pull = pullrequests.new_pullrequest(**kwargs)
    pull.repository.fetch()
    context['commits'] = pull.repository.commits
    context['diff'] = pull.repository.diff
    #generate_base_context(context)
    return context


def generate_base_context(context):
    project = context['project']
    repository = project.repository
    branches = repository.list_branches()
    tags = repository.list_tags()
    context['branches'] = branches
    context['tags'] = tags

    reference = context['reference']
    if reference in branches:
        context['current_reference_type'] = 'branch'
        context['current_reference'] = reference
        return
    elif reference in tags:
        context['current_reference_type'] = 'tag'
        context['current_reference'] = reference
        return
    t = repository.resolve_type(reference)
    if t != 'commit':
        raise
    c = repository.resolve_commit(reference)
    context['current_reference_type'] = 'tree'
    context['current_reference'] = c.hex
