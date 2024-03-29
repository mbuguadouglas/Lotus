from flask import Flask, Blueprint

def create_app():
	# initialize the flask app
	app = Flask(__name__)
	app.config['SECRET_KEY'] = '@Th3NorthR3m3mbers'	#set secret key for encrypting sessions


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

	# from .models import

	return app
