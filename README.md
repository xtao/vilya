CODE 1.0
========

A git repository hosting service and social coding collaboration service.

Quickstart
----------

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
echo "create database vilya1" | mysql -uroot
alembic upgrade head
python manage.py create_user
python wsgi.py
```

Override settings configuration
-------------------------------

```
mkdir -p instance
cp vilya/settings.cfg.example instance/settings.cfg
# then override configurations in instance/settings.cfg
```

Generate schema
---------------

```
alembic revision --autogenerate -m "blabla..."
alembic upgrade head
```

Frontend
--------

### Dependency
1. npm
2. rbenv(or rvm, ruby)

### Install tools

```
npm install coffee-script
gem install sass chunky_png fssm compass
```

Maybe you need:

`RBENV_VERSION="2.0.0-p247" python wsgi.py`

### rbenv

https://github.com/sstephenson/rbenv

```
curl https://raw.githubusercontent.com/fesplugas/rbenv-installer/master/bin/rbenv-installer | bash
export PATH=”$HOME/.rbenv/bin:$PATH”
eval "$(rbenv init -)"
unset RUBYOPT
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile
echo 'unset RUBYOPT' >> ~/.bash_profile
rbenv install 2.0.0-p247
rbenv rehash
```
