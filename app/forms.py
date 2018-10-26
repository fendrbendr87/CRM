from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Prospects, Clients
from app.queryfunc import select_prospect
from app import app, db


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        username = User.query.filter_by(username=username.data).first()
        if username is not None:
            raise ValidationError('Please use a different email address.')
 
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class AddProspectForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_cell = IntegerField('Cell Number', validators=[DataRequired()])
    submit = SubmitField('Add Prospect')

class ModifyProspectForm(FlaskForm):
    modified_first_name = StringField('First Name', validators=[DataRequired()])
    modified_last_name = StringField('Last Name', validators=[DataRequired()])
    modified_phone_cell = IntegerField('Cell Number', validators=[DataRequired()])
    submit = SubmitField('Update Prospect Information')


class AddClientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_cell = IntegerField('Cell Number', validators=[DataRequired()])
    submit = SubmitField('Add Client')

class ModifyClientForm(FlaskForm):
    modified_first_name = StringField('First Name', validators=[DataRequired()])
    modified_last_name = StringField('Last Name', validators=[DataRequired()])
    modified_phone_cell = IntegerField('Cell Number', validators=[DataRequired()])
    submit = SubmitField('Update Client Information')