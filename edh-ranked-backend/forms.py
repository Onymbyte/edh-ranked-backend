from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class CreateListingForm(FlaskForm):
    name = StringField('Commander Card name', validators=[DataRequired()])
    submit = SubmitField('Add Commander')
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=280)])
    submit = SubmitField('Add Comment')

class PlayRatingForm(FlaskForm):
    stars = RadioField('Stars', choices=[1,2,3,4,5], validate_choice=True, validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Optional(), Length(max=280)])
    submit = SubmitField('Add/Edit Play Rating')
class EnemyRatingForm(FlaskForm):
    stars = RadioField('Stars', choices=[1,2,3,4,5], validate_choice=True, validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Optional(), Length(max=280)])
    submit = SubmitField('Add/Edit Enemy Rating')
class ColorIdentityForm(FlaskForm):
    white = BooleanField('w')
    blue = BooleanField('u')
    black = BooleanField('b')
    red = BooleanField('r')
    green = BooleanField('g')
    submit = SubmitField('By Colors')
class AddCardForm(FlaskForm):
    name = StringField('Suggest Card name', validators=[DataRequired()])
    submit = SubmitField('Suggest Card')
class AddCardRatingForm(FlaskForm):
    stars = RadioField('Stars', choices=[1,2,3,4,5], validate_choice=True, validators=[DataRequired()])
    submit = SubmitField('Add/Edit Card Rating')