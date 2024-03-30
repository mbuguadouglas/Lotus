from flask import Flask, Blueprint, render_template


auth = Blueprint('auth',__name__)


@auth.route('signup', methods=['GET','POST'])
def signup():

	return render_template('signup.html')

@auth.route('login', methods=['GET','POST'])
def login():

	return render_template('login.html')

@auth.route('logout', methods=['GET','POST'])
def logout():

	return render_template('logout.html')
