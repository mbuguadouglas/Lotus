from flask import Flask, Blueprint

def create_app():
	# initialize the flask app
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '@Th3NorthR3m3mbers'	#set secret key for encrypting sessions



	return app
