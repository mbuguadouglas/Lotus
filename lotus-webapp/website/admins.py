from flask import Flask, Blueprint, render_template, redirect
from flask_login import login_required, current_user, logout_user
from .forms import ShoppingItemsForm
from . import db 
from .models import Customer, Product, Order, Cart


admins = Blueprint('admins', __name__)


@admins.route('/add-items',methods=['GET','POST'])
@login_required
def add_items():
	if current_user.id == 1:
		form = ShoppingItemsForm()

		return render_template('add_items.html', user=current_user, form=form)

	
	# will run if user.id != 1
	print('You do not have clearance to acces this page')
	return render_template('error_404.html')

	return render_template('add_items.html', user=current_user)