from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_wtf import FlaskForm
from ..models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=20)
        ]
    )
    surname = StringField('Surname', validators=[
        DataRequired(),
        Length(min=2, max=20)
        ]
    )
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ]
    )
    phone = StringField('Phone', validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]    
    )
    password = PasswordField('Password', validators=[
            DataRequired(),
            Length(min=8, max=50)
        ]    
    )
    confirm_password = PasswordField('Confirm Password', validators=[
            DataRequired(),
            Length(min=8, max=50),
            EqualTo('password')
        ]    
    )
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password', validators=[
            DataRequired(),
            Length(min=8, max=50)
        ]    
    )
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=20)
        ]
    )
    surname = StringField('Surname', validators=[
        DataRequired(),
        Length(min=2, max=20)
        ]
    )
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ]
    )
    phone = StringField('Phone', validators=[
            DataRequired(),
            Length(min=3, max=20)
        ]    
    )
    picture = FileField('Update Profile Picture', validators=[
            FileAllowed(['jpg', 'png'])
        ]
    )
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Email()
        ]
    )
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
            DataRequired()
        ]
    )
    confirm_password = PasswordField('Confirm Password', validators=[ 
            DataRequired(), 
            EqualTo('password')
        ]
    )
    submit = SubmitField('Reset Password')