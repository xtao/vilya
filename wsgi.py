# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from sina import Sina
from sina.config import DEFAULT_CONFIG

from vilya import api, frontend
from vilya.middleware import GitDispatcher

frontend_app = frontend.create_app()
api_app = api.create_app()
DEFAULT_CONFIG['project_root'] = api_app.config['REPO_PATH']
DEFAULT_CONFIG['chunked'] = True
sina_app = Sina(DEFAULT_CONFIG)


application = DispatcherMiddleware(
    frontend_app,
    {'/api': api_app}
)
application = GitDispatcher(sina_app, application)

if __name__ == "__main__":
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
