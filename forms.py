from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    email = StringField('Email ', [validators.InputRequired()])
    password = PasswordField('Password ', [validators.InputRequired()])

class AddConcert(FlaskForm):
    band_name = StringField('Band or Artist Name', [validators.InputRequired()])
    genre = StringField('Genre')
    date = StringField('Date')
    venue = StringField('Venue')
    location = StringField('City')
    band_pic_path = StringField('Photo URL')

class AddBucketList(FlaskForm):
    band_name = StringField('Band or Artist Name', [validators.InputRequired()])
    genre = StringField('Genre')
    band_pic_path = StringField('Photo URL')

