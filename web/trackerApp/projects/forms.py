from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class StartProjectForm(FlaskForm):

    title = StringField("Project Name", validators=[DataRequired()])
    description = TextAreaField("Project Description")
    submit = SubmitField("Start Project")
