from flask_wtf import FlaskForm
from model import Users
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError



class RegistrationForm(FlaskForm):

	username = StringField('Username', 
		validators=[DataRequired(), Length(min=2, max=50)])

	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Register')
	def validate_username(self, username):
		user = Users.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That is username already taken, try different username')


class LoginForm(FlaskForm):

	username = StringField('Username', 
		validators=[DataRequired()])

	password = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

