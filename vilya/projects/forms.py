# -*- coding: utf-8 -*-

from flask_wtf import Form, TextField, Required, Optional

__all__ = ['NewProjectForm', 'UpdateProjectForm']


class NewProjectForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])


class UpdateProjectForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])
