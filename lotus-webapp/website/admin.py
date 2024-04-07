from flask import Flask, Blueprint, render_template, redirect
from flask_login import login_required, current_user, logout_user
from .forms import ShoppingItemsForm
from . import db 
from .models import Customer, Product, Order, Cart


admin = Blueprint('admin', __name__)


@admin.route('/',methods=['GET','POST'])
@login_required
def add_items():
	if current_user.id == 1:
		print('welcome to the admin panel')
		return render_template('admin.html', user=current_user)

	else:
		print('You do not have clearance to acces this page')
		return render_template('error_404.html')

	return render_template('admin.html', user=current_user)