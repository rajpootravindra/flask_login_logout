from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flaskblog.models import User
from  wtforms.validators import ValidationError
from flask_login import  current_user
from flask_wtf.file import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("username is already taken, Please choose diffrent one.")


    def validate_email(self, email):
        email=User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email is already taken, Please choose diffrent one.")

class LoginForm(FlaskForm):
    email = StringField('Email',         validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class to update the user account. 

class UpdateAccountForm(FlaskForm):
    # we will make two fields to update the username and email field. 
    username = StringField('Username',              validators=[DataRequired(), Length(min=2, max=20)])
    email =    StringField('Email',                 validators=[DataRequired(), Email()])
    image_file =  FileField("udpate profile Picture",  validators=[FileAllowed(['jpg','jpeg', 'png'])])
    submit =   SubmitField('Update')

    # create a function to validate the fields of the form to check if the username and email is alredy taken.
    # to do this we will also have to import the library ,     from flask_login import current_user,   at the top of this file. 
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("Username already taken , please choose a different one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("Email id already taken , please choose a different one.")


# next step is to create a form.  inside the forms.py file as a class. 


class PostForm(FlaskForm):
    title = StringField("Title" ,   validators=[DataRequired()])
    post_image =  FileField("Add post picture",  validators=[FileAllowed(['jpg','jpeg', 'png'])])
    content = TextAreaField("Content" , validators= [DataRequired()])
    submit= SubmitField("Add Post")
