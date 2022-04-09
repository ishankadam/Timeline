from lib2to3.pgen2.token import OP
from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,SelectField,DateField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError,Optional
from wtforms.validators import NumberRange
from flask_wtf.file import FileField,FileAllowed,FileRequired
import re
from datetime import date
class RegistrationForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2, max=20, message='Name length must be between %(min)d and %(max)dcharacters')])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, message="Password be at least 8 characters")])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    contact = StringField('Contact',
        validators=[DataRequired(), Length(min=10, max=10) ])
    internship = StringField('internship',
        validators=[DataRequired()], render_kw={"placeholder": "Internship (IF ANY)"})
    certificate = StringField('Certification',
        validators=[DataRequired() ],render_kw={"placeholder": "Certification (IF ANY)"})    
    resume = FileField('resume',
        validators=[FileRequired(),FileAllowed(['pdf'], "Wrong format!")])    
    upload = SubmitField('upload')                       
    submit = SubmitField('Sign Up') 
    
    def validate_name(self, name):
        excluded_chars = " @*?!'^+%&/()=}][{$#"
        for char in self.name.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")
    
    def validate_password(self, password):
        password = self.password.data
        if len(password)< 4:
            raise ValidationError('Password must be at lest 8 letters long')
        elif re.search('[0-9]',password) is None:
            raise ValidationError('Password must contain a number')
        elif re.search('[A-Z]',password) is None:
            raise ValidationError('Password must have one uppercase letter')
        elif re.search('[a-z]',password) is None:
            raise ValidationError('Password must have one lowercase letter') 
                

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')