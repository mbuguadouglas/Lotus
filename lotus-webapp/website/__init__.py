from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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


	# initialize the login manager for session and token mngmt
	login_manager = LoginManager()
	login_manager.init_app(app)
	login_manager.login_view = 'auth.login'		#what does this do? Tell app where login view is. If user is not logged in redirect here. Else returns an error
	# login_manager.login_message = 'We wacha zako buana'
	login_manager.login_message_category = 'danger'		#categorize login error message

	# user loader function for the login manager. load user based on unique identifier(id)
	@login_manager.user_loader
	def load_user(id):
		""" function to automatically 
		look up the db searchig if users primary is present
		"""
		return Customer.query.get(int(id))


	# when user tries accessing url not in our flask app they get this html returned
	@app.errorhandler(404)
	def page_not_found(error):
		return render_template('error_404.html')


	# create he database within the app context
	with app.app_context():
		create_database(app)


	# import all related .py files as modules
	from .auth import auth
	from .views import views
	from .models import Customer, Product, Cart, Order
	from .admin import admin

	# register the various blueprints
	app.register_blueprint(auth, url_prefix='/auth')	#localhost:5000/auth/<route>
	app.register_blueprint(views, url_prefix='/')	#localhost:5000/<route>
	app.register_blueprint(admin, url_prefix='/admin')	#localhost:5000/admin/<route>
	# app.register_blueprint(auth)
	# app.register_blueprint(views)
	# app.register_blueprint(admin)




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
