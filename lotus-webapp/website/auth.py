from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Customer

auth = Blueprint('auth',__name__)


@auth.route('signup', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		email = request.form.get('email')
		username = request.form.get('username')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')

		# check if the user already exists in the db
		customer = Customer.query.filter_by(email=email).first()

		# if user exists
		if customer:
			message = 'This user already exists'
			flash(message, category='warning')
		elif len(email) <= 7 or len(email) >= 30:
			message = "Oops! Looks like the email you entered is not valid. Please try again"
			flash(message, category='warning')
		elif len(username) <= 3:
			message = 'Oops! Usernames must be at least 3 characters long. Please try again'
			flash(message, category='warning')
		# password logic for special caharacters? cpital letter, e.t.c
		elif len(password1) <= 5:
			message = 'Oops! Passwords must be at least 3 characters long. Please try again'
			flash(message, category='warning')
		elif password1 != password2:
			message = "Oops! Looks like the passwords you entered don't match. Try typing them again."
			flash(message, category='warning')
		else:
			message = 'Congratulations! You have successfuly created an account'
			flash(message, category='success')

			new_customer = Customer(email=email, name=username, password_hash=password1)#,date_joined=?)
			db.session.add(new_customer)
			db.session.commit()

			return redirect(url_for('views.index'))

	return render_template('signup.html')

@auth.route('login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		# get the email and password values from the form
		email = request.form.get('email')
		password = request.form.get('password')

		# Check if the user exists in the db
		customer = Customer.query.filter_by(email=email).first()

		# check if customer exists in db
		if customer:
			# if customer does exist in db, check if passwords match
			if Customer.password(password) == cutomer.password_hash:
				message = 'Congratulations! You have successfuly logged in.'
				flash(message, category='success')

				return redirect(url_for('views.index'))


			elif not Customer.verify_password(password):	#return true if passwords match
				message = 'Oops! Looks like you entered the wrong password. Please check and try again.'
				flash(message, category='warning')

		else:
			message = 'Oops! Looks like the user does not exist. Maybe you could try signing up instead?'
			flash(message, category='warning')


	return render_template('login.html')

@auth.route('logout', methods=['GET','POST'])
def logout():

	return render_template('logout.html')
