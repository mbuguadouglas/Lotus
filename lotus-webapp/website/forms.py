from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, FloatField, BooleanField, PasswordField, EmailField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Length, EqualTo
from flask_wtf.file import FileField, FileRequired


class SignupForm(FlaskForm):
	email = EmailField('Enter Email', validators=[InputRequired(), Length(min=7, max=30)])
	username = StringField('Enter Username', validators=[InputRequired(), Length(min=3)])
	password1 = PasswordField('Enter Password', validators=[InputRequired(), Length(min=5)])
	password2 = PasswordField('Confirm Password', validators=[InputRequired(),  EqualTo('password1'), Length(min=5)])

	signup = SubmitField('Sign Up')


class LoginForm(FlaskForm):
	email = EmailField('Email Address', validators=[InputRequired(), Length(min=7, max=20)])
	password = PasswordField('Enter Password', validators=[InputRequired(), Length(min=5)])
	login = SubmitField('Login')

# 	# instead of redifining them like this, i will make it inherit from the signup form

class ChangePasswordForm(FlaskForm):
	current_password = PasswordField('Enter Password', validators=[InputRequired(), Length(min=5)])
	new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=5)])
	confirm_new_password = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('new_password'), Length(min=5)])
	submit = SubmitField('Change Password')

class ShoppingItemsForm(FlaskForm):
	# all needed inputs
	product_name = StringField('Name of Product', validators=[DataRequired()]) 
	current_price = FloatField('Current price of product', validators=[DataRequired()]) 
	previous_price = FloatField('Previous price of product', validators=[DataRequired()]) 
	in_stock = IntegerField('In stock', validators=[DataRequired(), NumberRange(min=0)])
	product_pic = FileField('Product picture', validators=[FileRequired()])
	flash_sale = BooleanField('Flash sale?')

	# buttons
	add_product = SubmitField('Add product')
	update_product = SubmitField('Update product')









