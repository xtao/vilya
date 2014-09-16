# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired as Required
from wtforms.validators import Optional

__all__ = ['NewPullRequestForm', 'UpdatePullRequestForm']


class NewPullRequestForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])
    origin = TextField('Origin', validators=[Required()])
    upstream = TextField('Upstream', validators=[Required()])



class UpdatePullRequestForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])
