from flask import Flask, Blueprint


auth = Blueprint('auth',__name__)


@auth.route('signup', methods=['GET','POST'])
def signup():

	return '<h1>The signup page!</h1>'

@auth.route('login', methods=['GET','POST'])
def login():

	return '<h1>The login page!</h1>'

@auth.route('logout', methods=['GET','POST'])
def logout():

	return '<h1>The logout page!</h1>'
