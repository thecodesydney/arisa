from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, StringField, BooleanField, SubmitField
from wtforms.validators import Email, InputRequired, Length, ValidationError, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Please enter your email')])
    password = PasswordField('Password', validators=[InputRequired('Please enter your password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AgentRegisterForm(FlaskForm):
    email = StringField('Email (username)', validators=[InputRequired(),
                                                        Email(message='Please provide a valid email.'), Length(max=45)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=45)])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])
    phone = StringField('Phone', validators=[InputRequired(), Length(max=45)])
    agency_name = StringField('Agency Name', validators=[InputRequired(), Length(max=45)])
    submit = SubmitField('Register')
    recaptcha = RecaptchaField()

    # constrained the user email to be unique in the system as it is the username for login.
    def validate_agent_email(self, agent_email):
        user = User.query.filter_by(email=agent_email.data).first()
        if user:
            raise ValidationError('This user email is already taken. Please use another.')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
