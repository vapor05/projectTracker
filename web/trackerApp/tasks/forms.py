from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddTaskForm(FlaskForm):

    title = StringField("Task Title", validators=[DataRequired()])
    description = TextAreaField("Task Description")
    submit = SubmitField("Add Task")
