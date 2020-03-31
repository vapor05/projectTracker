from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddItemForm(FlaskForm):

    title = StringField("Work Item Title", validators=[DataRequired()])
    description = TextAreaField("Work Item Description")
    submit = SubmitField("Add Work Item")
