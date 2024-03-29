from flask import Flask, Blueprint


views = Blueprint('views',__name__)


@views.route('/',methods=['GET','POST'])
def index():

	return '<h1> This is the home page</h1>'