# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired as Required
from wtforms.validators import Optional


__all__ = ['NewProjectForm', 'UpdateProjectForm']


class NewProjectForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])


class UpdateProjectForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])
