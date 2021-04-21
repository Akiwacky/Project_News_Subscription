from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import InputRequired, EqualTo, length


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Please Add A Username"),
                                                   length(4, 20, message="Username's length is not accurate. Minimum "
                                                                         "length: 4, Maximum length: 20")])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm',
                                                                              message="Passwords must match")])
    confirm = PasswordField('Confirm Password')
    frequency = SelectField('Frequency', validators=[InputRequired(message="Select how frequent we should message you")],
                            choices=[("D", "Daily"), ("W", "Weekly"), ("M", "Monthly")])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()


class EditForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Please Add A Username"),
                                                   length(4, 20, message="Username's length is not accurate. Minimum "
                                                                         "length: 4, Maximum length: 20")])
    frequency = SelectField('Frequency',
                            validators=[InputRequired(message="Select how frequent we should message you")],
                            choices=[("D", "Daily"), ("W", "Weekly"), ("M", "Monthly")])
    submit = SubmitField()
