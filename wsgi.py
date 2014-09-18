# -*- coding: utf-8 -*-

import os
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from sina import Sina
from sina.config import DEFAULT_CONFIG

from vilya import api, frontend
from vilya.middleware import GitDispatcher

frontend_app = frontend.create_app()
api_app = api.create_app()
PROJECT_ROOT = api_app.config['REPO_PATH']
DEFAULT_CONFIG['project_root'] = PROJECT_ROOT
DEFAULT_CONFIG['chunked'] = True
sina_app = Sina(DEFAULT_CONFIG)


@sina_app.get_repo_path
def get_repo_path_handler(environ, path):
    with api_app.app_context():
        from vilya.services import users, projects
        user = users.get_by_name_path(path)
        if user:
            print user.name
        project = projects.get_by_name_path(path)
        return os.path.join(PROJECT_ROOT, project.path)


@sina_app.has_permission
def has_permission_handler(environ, path, perm):
    with api_app.app_context():
        from vilya.services import users, projects
        user = users.get_by_name_path(path)
        return True


application = DispatcherMiddleware(
    frontend_app,
    {'/api': api_app}
)
application = GitDispatcher(sina_app, application)

if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
