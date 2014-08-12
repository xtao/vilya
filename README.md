# Vilya

A python implementation of Git repository hosting service and social coding collaboration service

Originally inspring and adapting from douban's internal project CODE

## Quickstart
```
   $ virtualenv venv

   $ source venv/bin/activate

   $ pip install -r requirements.txt

   $ mysql -uroot

   $ create database vilya1

   $ alembic upgrade head

   $ python wsgi.py
```

## Override settings configuration
```
   $ mkdir /path/to/vilya/instance

   $ cd /path/to/vilya/instance

   $ touch settings.cfg

   override configurations in settings.cfg

