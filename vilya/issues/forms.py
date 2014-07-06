# -*- coding: utf-8 -*-

from flask_wtf import Form, TextField, Required, Optional

__all__ = ['NewIssueForm', 'UpdateIssueForm']


class NewIssueForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])


class UpdateIssueForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])
