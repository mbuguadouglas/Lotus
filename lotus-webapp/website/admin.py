from flask import Flask, Blueprint


admin = Blueprint('admin', __name__)

@admin.route('admin',methods=['GET','POST'])
def index():
	return '<h1> This is the admin page </h1>'