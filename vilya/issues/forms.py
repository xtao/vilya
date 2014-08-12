# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired as Required
from wtforms.validators import Optional

__all__ = ['NewIssueForm', 'UpdateIssueForm']


class NewIssueForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])


class UpdateIssueForm(Form):
    name = TextField('Name', validators=[Required()])
    description = TextField('Description', validators=[Optional()])
