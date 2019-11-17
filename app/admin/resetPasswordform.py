''''
This file is for form creation. The reset password form is read only form with below fields.
It will be have existing user and agent fields. Also, it has new system generated reset password.
Author - Chintan Patel
Date - 29/Sep/2019
'''

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class ResetPasswordForm(FlaskForm):
    userID = StringField('User ID', validators=[InputRequired(), Length(max=20)])
    agentID = StringField('Agent ID', validators=[InputRequired(), Length(max=20)])
    firstName = StringField('First Name', validators=[InputRequired(), Length(max=20)])
    lastName = StringField('Last Name', validators=[InputRequired(), Length(max=20)])
    phone = StringField('Phone', validators=[InputRequired(), Length(max=20)])
    agencyName = StringField('Agency Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Length(max=20)])
    roleName = StringField('Role Name', validators=[InputRequired(), Length(max=20)])
    newResetPassword = StringField('Reset Password', validators=[InputRequired(), Length(max=50)])
    #message = TextAreaField('Leave a message', validators=[InputRequired(), Length(max=400)])
    submit = SubmitField('Submit')
    #recaptcha = RecaptchaField()


