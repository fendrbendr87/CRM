from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, People
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

class AddPeopleForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone_cell = IntegerField('Cell Number', validators=[DataRequired()])
    ptype = SelectField('Client Type',  choices=[('buyer', 'Buyer'), 
        ('seller', 'Seller')], validators=[DataRequired()])
    pstatus = SelectField('Client Status', choices=[('prospect', 'Prospect'), 
        ('client', 'Client')], validators=[DataRequired()])
    house_number = StringField('House Number')
    street_name = StringField('Street Name')
    city_name = StringField('City Name')
    state_name = StringField('State Name')
    zip_code = StringField('Zip Code')
    notes = StringField('Notes')
    submit = SubmitField('Add Person')

class ModifyPeopleForm(FlaskForm):
    modified_first_name = StringField('First Name', validators=[DataRequired()])
    modified_last_name = StringField('Last Name', validators=[DataRequired()])
    modified_phone_cell = IntegerField('Cell Number', validators=[DataRequired()])
    modified_ptype = SelectField('Client Type',  choices=[('buyer', 'Buyer'), 
        ('seller', 'Seller')], validators=[DataRequired()])
    modified_pstatus = SelectField('Client Status', choices=[('prospect', 'Prospect'), 
        ('client', 'Client')], validators=[DataRequired()])
    modified_house_number = StringField('House Number')
    modified_street_name = StringField('Street Name')
    modified_city_name = StringField('City Name')
    modified_state_name = StringField('State Name')
    modified_zip_code = StringField('Zip Code')
    modified_notes = StringField('Notes')
    modified_price = IntegerField('Price')
    submit = SubmitField('Update Person\'s Information')

class SearchPeopleForm(FlaskForm):
    first_last = StringField('First or Last Name', validators=[DataRequired()])
    submit = SubmitField('Search for Person')

class AddProfileNotesForm(FlaskForm):
    pnotes = TextAreaField('Add notes here')
    submit = SubmitField('Add Profile Notes')

class ConvertClientForm(FlaskForm):
    submit = SubmitField('Convert Client')