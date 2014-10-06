# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired as Required

__all__ = ['NewCommentForm', 'UpdateCommentForm']


class NewCommentForm(Form):
    description = TextField('Description', validators=[Required()])


class UpdateCommentForm(Form):
    description = TextField('Description', validators=[Required()])
