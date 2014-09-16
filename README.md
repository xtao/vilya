CODE 1.0
========

A git repository hosting service and social coding collaboration service.

Quickstart
----------

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ mysql -uroot
$ create database vilya1
$ alembic upgrade head
$ python manager.py create_user
$ python wsgi.py
```

Override settings configuration
-------------------------------

```
$ mkdir /path/to/vilya/instance
$ cd /path/to/vilya/instance
$ touch settings.cfg
override configurations in settings.cfg
```

Generate Schema
---------------

```
$ alembic revision --autogenerate -m “Added pullrequest”
$ alembic upgrade head
```

