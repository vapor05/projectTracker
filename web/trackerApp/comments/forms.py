from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddCommentForm(FlaskForm):

    comment = TextAreaField("Note Text")
    submit = SubmitField("Add Note")
