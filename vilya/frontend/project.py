# -*- coding: utf-8 -*-

from flask import (Blueprint,
                   render_template,
                   flash,
                   redirect,
                   url_for)
from flask.ext.login import current_user
from ..services import projects, users, pullrequests
from ..forms import NewProjectForm, NewPullRequestForm
from . import route

bp = Blueprint('project', __name__)


@route(bp, '/new')
def new():
    context = {}
    context['form'] = NewProjectForm()
    return render_template('projects/new.html', **context)


@route(bp, '/create', methods=['POST'])
def create():
    """Create a new project."""
    form = NewProjectForm()
    if form.validate_on_submit():
        p = projects.create(owner_id=current_user.id, **form.data)
        flash('New project was successfully created!', 'info')
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
    context['path'] = None

    if project.repository.is_empty:
        context['project_menu'] = 'Code'
        return render_template('projects/empty.html', **context)

    context['reference'] = project.repository.head.name
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
    context['u_name'] = u_name
    context['p_name'] = p_name

    if project.repository.is_empty:
        return redirect(url_for('.index',
                                u_name=u_name,
                                p_name=p_name))

    context['form'] = NewPullRequestForm()
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
    generate_reference_context(context)
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
    generate_reference_context(context)
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
    generate_reference_context(context)
    return context


def generate_commit_context(context):
    context['project_menu'] = 'Commits'
    project = context['project']
    reference = context['reference']

    commit = project.repository.resolve_commit(reference=reference)
    context['commit'] = commit
    context['diff'] = project.repository.diff(commit.hex)
    generate_base_context(context)
    generate_reference_context(context)
    return context


def generate_compare_context(context):
    kwargs = {}
    project = context['project']
    reference = context['reference']

    # compare/<to>
    from_reference = project.repository.head.name
    to_reference = reference

    # compare/<from...to>
    if '...' in reference:
        from_reference, _, to_reference = reference.partition('...')
    # upstream - base, origin - head
    kwargs['upstream'] = from_reference
    kwargs['origin'] = to_reference
    kwargs['project'] = project
    pull = pullrequests.new_pullrequest(**kwargs)
    pull.repository.fetch()
    context['commits'] = pull.repository.commits
    context['diff'] = pull.repository.diff

    # range editor
    if ':' in from_reference:
        name, _, upstream_branch = from_reference.partition(':')
        upstream = projects.get_by_user_name(name, project)
    else:
        upstream_branch = from_reference
        upstream = project
    context['upstream_project'] = upstream
    context['upstream_branch'] = upstream_branch
    upstream_projects = projects.find_forked(project)
    context['upstream_projects'] = upstream_projects
    upstream_projects_menu = []
    for p in upstream_projects:
        upstream_projects_menu.append(['%s/compare/%s...%s' % (upstream.full_name, upstream_branch, to_reference), p])
    context['upstream_projects_menu'] = upstream_projects_menu
    upstream_branches = upstream.repository.list_branches()
    context['upstream_branches'] = upstream_branches
    upstream_branches_menu = []
    for b in upstream_branches:
        upstream_branches_menu.append(['%s/compare/%s...%s' % (upstream.full_name, b.name, to_reference), b])
    context['upstream_branches_menu'] = upstream_branches_menu

    if ':' in to_reference:
        name, _, origin_branch = to_reference.partition(':')
        origin = projects.get_by_user_name(name, project)
    else:
        origin_branch = to_reference
        origin = project
    context['origin_project'] = origin
    context['origin_branch'] = origin_branch
    origin_projects = projects.find_forked(project)
    context['origin_projects'] = origin_projects
    origin_projects_menu = []
    for p in origin_projects:
        if p.id == project.id:
            branch = origin_branch
        else:
            branch = "%s:%s" % (p.owner.name, origin_branch)
        origin_projects_menu.append(['%s/compare/%s...%s' % (upstream.full_name, from_reference, branch), p])
    context['origin_projects_menu'] = origin_projects_menu
    origin_branches = origin.repository.list_branches()
    context['origin_branches'] = origin_branches
    origin_branches_menu = []
    for b in origin_branches:
        if origin.id == project.id:
            branch = b.name
        else:
            branch = "%s:%s" % (p.owner.name, b.name)
        origin_branches_menu.append(['%s/compare/%s...%s' % (upstream.full_name, from_reference, branch), b])
    context['origin_branches_menu'] = origin_branches_menu

    generate_base_context(context)
    return context


def generate_base_context(context):
    project = context['project']
    repository = project.repository
    branches = repository.list_branches()
    tags = repository.list_tags()
    context['branches'] = branches
    context['tags'] = tags

    if project.upstream_id:
        context['forked_from_project'] = project.upstream


def generate_reference_context(context):
    project = context['project']
    repository = project.repository
    branches = context['branches']
    tags = context['tags']
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
