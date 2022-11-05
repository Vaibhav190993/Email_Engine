from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import current_user
from models import User
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class SendEmailForm(FlaskForm):
    email = StringField(
        validators=[
            InputRequired(), Length(min=4, max=50)],
        render_kw={"placeholder": "email"}
    )
    subject = StringField(
        validators=[
            InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "subject"}
    )

    message = TextAreaField(
        validators=[InputRequired()],
        render_kw={"placeholder": "message"}
    )

    submit = SubmitField('Send')

    def validdate_email(self, email):
        if email.data != regex:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('The usernamer is taken. Please choose a  different username.')

class RegistrationForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(), Length(min=4, max=120)],
        render_kw={"placeholder": "Enter Your Username"}
    )
    password = PasswordField(
        validators=[InputRequired(),
                    Length(min=4, max=16)],
        render_kw={"placeholder": "Password"}
    )

    # confirm_password = PasswordField(
    #     validators=[InputRequired(),EqualTo(password)],
    #     render_kw={"placeholder": "Confirm Password"}
    # )

    submit = SubmitField('Sign Up')

    def validdate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The usernamer is taken. Please choose a  different username.')


class LoginForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"}
    )

    password = PasswordField(
        validators=[InputRequired(),
                    Length(min=4, max=10)],
        render_kw={"placeholder": "Password"}
    )

    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(), Length(min=4, max=120)],
    )

    submit = SubmitField('Update')

    def validdate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The usernamer is taken. Please choose a  different username.')

