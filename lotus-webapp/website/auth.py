from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import SignupForm, LoginForm, ChangePasswordForm
from . import db
from .models import Customer


auth = Blueprint('auth',__name__)



@auth.route('signup', methods=['GET','POST'])
def signup():
	""" function that defines the authentication process for signup
	chose not to use wtf_forms since one cannot style them. They're
	hiddeous. Might take up the callenge of rectifying this as an open source
	project
	** took it up. not so bad**
	**chose to change entire code base to wtforms!**
	"""

	form = SignupForm()

	# if request.method == 'POST':
	if form.validate_on_submit():
		email = form.email.data
		username = form.username.data
		password1 = form.password1.data
		password2 = form.password2.data

		# check if the user already exists in the db
		customer = Customer.query.filter_by(email=email).first()

		# if user exists
		if customer:
			message = 'Oops! Looks like this user already exists. Try logging in instead?'
			flash(message, category='warning')
		else:
			# try catch block foe error handling when adding a user to the database
			try:
				new_customer = Customer(email=email, name=username, password=generate_password_hash(password1))#,date_joined=?)
				db.session.add(new_customer)
				db.session.commit()

				message = 'Congratulations! You have successfuly created an account'
				flash(message, category='success')
			except Exception as e:
				print (e)
				message = 'Oops! Looks like the account could not be created. Try again?'
				flash(message, category='warning')

			login_user(new_customer)
			return redirect(url_for('views.index'))

	return render_template('signup.html', user=current_user, form=form)



@auth.route('login', methods=['GET','POST'])
def login():

	form = LoginForm()

	# if request.method == 'POST':
	if form.validate_on_submit():
		# get the email and password values from the form
		email = form.email.data
		password = form.password.data

		# Check if the user exists in the db
		customer = Customer.query.filter_by(email=email).first()

		# check if customer exists in db
		if customer:
			# if customer does exist in db, check if passwords match
			if check_password_hash(customer.password, password):

				login_user(customer, remember=True)

				message = 'Congratulations! You have successfuly logged in.'
				flash(message, category='success')

				login_user(customer)
				return redirect(url_for('views.index'))


			elif not check_password_hash(customer.password, password):	#verification using werkzeug in auth.py
			# else:				#using werkzeug in models.py-----return true if passwords dont match
				message = 'Oops! Looks like you entered the wrong password. Please check and try again.'
				flash(message, category='warning')

		else:
			message = 'Oops! Looks like the user does not exist. Maybe you could try signing up instead?'
			flash(message, category='warning')


	return render_template('login.html', user=current_user, form=form)



@auth.route('logout', methods=['GET','POST'])
@login_required
def logout():

	logout_user()

	message = 'Oh no! Looks like you have been logged out of you account. Try logging back in.'
	flash(message, category='danger')

	return redirect(url_for('auth.login'))



# route for the profile page
@auth.route('profile/<int:customers_id>', methods=['GET','POST'])
@login_required
def profile(customers_id):	#why not user.id?!?!
	# print (f'Customer id is: {customers_id}')
	# return f'Customer id is: {customers_id}'
	customer = Customer.query.get(customers_id)	#-> instaed of doing this use current_user functionality from flask_login in the front end

	# basic error handling to see the url
	# print(url_for('auth.profile(customers_id)')) #-> couldnt get it to work
	# print(redirect('/profile/int:<customers_id>'))	#worked flawlessly
	# print(redirect('profile/int:<customers_id>'))	#worked flawlessly
	# print(customer.password)	#this password is hashed

	return render_template('profile.html', user=current_user)#, customer=customer)



@auth.route('profile/change-password/<int:customers_id>', methods=['GET','POST'])
@login_required
def change_password(customers_id):

	form = ChangePasswordForm()

	if request.method == 'POST':
		current_password = form.current_password.data
		new_password = form.new_password.data
		confirm_new_password = form.confirm_new_password.data

		# get the customer from the database
		customer = Customer.query.get(customers_id)

		if check_password_hash(customer.password, current_password):
			# print('Ahaa! Password inputed and that in db finally match')
			if new_password == confirm_new_password:
				# print('new and confirmed password match')
				customer.password = generate_password_hash(confirm_new_password)
				db.session.commit()
				# print('change commited to db')

				message = 'Congratulations! You have succesfully updated your password.'
				flash(message, category='success')

				# return redirect('/') -> works!!
				# return redirect('login') -> does not work!!
				# return redirect(f'profile/{customer.id}') -> doesnt work!!
				# return redirect(url_for('auth.profile')) -> doesnt work!!
				# return redirect(f'/auth/profile/<int:customers_id>') -> does not work!
				return redirect(f'/auth/profile/{customer.id}')

			else:
				# print("Oh no! New passwords don't match")
				message = 'Oops! Looks like the new and confirmed passwords do not match. Look and try again?'
				flash(message, category='danger')
		else:
			# print('Password inputed does not match that in the db')
			message = 'Oops! Looks like the current password entered is incorrect.'
			flash(message, category='danger')

	return render_template('change_password.html', user=current_user, form=form)
