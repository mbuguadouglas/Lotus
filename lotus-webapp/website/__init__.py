from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
# from os import path

db = SQLAlchemy()
db_name = 'db.sqlite3'


def create_app():
	""" function to runn the application"""

	# initialize the flask app
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '@Th3NorthR3m3mbers'	#set secret key for encrypting sessions
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

	db.init_app(app)	#initialize database

	# import the various blueprints and register them
	from .auth import auth
	# app.register_blueprint(auth)
	app.register_blueprint(auth, url_prefix='/auth')	#localhost:5000/auth/<route>

	from .views import views
	# app.register_blueprint(views)
	app.register_blueprint(views, url_prefix='/')	#localhost:5000/<route>

	from .admin import admin
	# app.register_blueprint(admin)
	app.register_blueprint(admin, url_prefix='/admin')	#localhost:5000/admin/<route>

	from .models import Customer, Product, Cart, Order
	with app.app_context():
		create_database(app)


	return app


def create_database(app):
	db.create_all()
	print('Database created successfully!')


# # FUNCTION TO CREATE DB. MUST IMPORT OS PATH
# # FIND WHAT IS THE DIFFERENCE BTWN THE TWO AND WHICH IS BETTER FOR OPTIMIZATION
# def create_database(app):
# 	"""function to create the database"""

# 	with app.app_context():
# 		if not path.exists('website'+db_name):
# 			db.create_all()
# 			print ('created database succesfully!')
# 		else:
# 			print ('An error occurred during database creation')
