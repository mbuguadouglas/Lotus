from flask import Flask, Blueprint, render_template, redirect, flash, send_from_directory
from flask_login import login_required, current_user, logout_user
from .forms import ShoppingItemsForm
from . import db 
from .models import Customer, Product, Order, Cart
from werkzeug.utils import secure_filename


admins = Blueprint('admins', __name__)



# create route to view items in the database
@admins.route('products/<path:filename>')	#filepath of where the images are located
def display_items(filename):				#take the filename as a parameter

	product_image = send_from_directory('../products',filename)		#move 1 step outward to given folder, and find the filename
	return product_image


@admins.route('add-items',methods=['GET','POST'])
@login_required
def add_items():
	if current_user.id == 1:
		form = ShoppingItemsForm()

		if form.validate_on_submit():
			product_name = form.product_name.data
			current_price = form.current_price.data
			previous_price = form.previous_price.data
			category = form.category.data
			in_stock = form.in_stock.data
			flash_sale = form.flash_sale.data
			add_product = form.add_product.data
			update_product = form.update_product.data

			# file = form.product_pic.data
			product_pic = form.product_pic.data
			file_name = secure_filename(product_pic.filename)	#removes invalid characters from filenames e.g _, %, $
			print(f'file name is {file_name}')

			# setup directory to be storing our files
			file_path = f'./products/{file_name}'
			product_pic.save(file_path)
			print('file saved successfuly')

			new_item = Product(name=product_name, picture=file_path, current_price=current_price, past_price=previous_price, category=category, instock=in_stock, flash_sale=flash_sale)
			
			try:
				# save new product to database
				db.session.add(new_item)
				db.session.commit()
				print('file commited to db')

				message = f'The {product_name} has been added succesfully!'
				flash(message, category='success')
				print('Product added!')

				return render_template('add_items.html', form=form, user=current_user)

			except Exception as e:
				print(e)
				print('something went wrong')

				message = f'The {product_name} has not been added to the catalogue. Try again?'
				flash(message, category='danger')


		return render_template('add_items.html', user=current_user, form=form)

	
	# will run if user.id != 1
	print('You do not have clearance to acces this page')
	return render_template('error_404.html', user=current_user)


@admins.route('view-items', methods=['GET', 'POST'])
@login_required
def view_items():
	if current_user.id == 1:

		items = Product.query.order_by(Product.date_added).all()

		return render_template('view_items.html', user=current_user, items=items)


	return render_template('error_404.html',user=current_user)


@admins.route('update-items/<int:item_id>', methods=['GET','POST'])
def update_items(items_id):

	return render_template('error_404.html', user=current_user)


@admins.route('delete-items/<int:item_id>', methods=['GET','POST'])
def delete_items(items_id):


	return render_template('error_404.html', user=current_user)









