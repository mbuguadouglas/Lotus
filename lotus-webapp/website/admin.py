from flask import Flask, Blueprint, render_template, redirect, flash, send_from_directory
from flask_login import login_required, current_user, logout_user
from .forms import ShoppingItemsForm
from . import db 
from .models import Customer, Product, Order, Cart
from werkzeug.utils import secure_filename


admin = Blueprint('admin', __name__)



# create route to view items in the database
@admin.route('products/<path:filename>')	#filepath of where the images are located
def display_items(filename):				#take the filename as a parameter

	product_image = send_from_directory('../products',filename)		#move 1 step outward to given folder, and find the filename
	return product_image


@admin.route('add-items',methods=['GET','POST'])
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



@admin.route('view-items', methods=['GET', 'POST'])
@login_required
def view_items():
	if current_user.id == 1:

		items = Product.query.order_by(Product.date_added).all()

		return render_template('view_items.html', user=current_user, items=items)


	return render_template('error_404.html',user=current_user)




@admin.route('update-items/<int:item_id>', methods=['GET','POST'])
def update_items(item_id):

	if current_user.id == 1:
		form = ShoppingItemsForm()

		# get the items from the database
		item_to_update = Product.query.get(item_id)

		# using the wtforms keyword placeholder. set the already existing value to be displayed on the form as a placeholder
		form.product_name.render_kw = {'placeholder': item_to_update.name}
		form.previous_price.render_kw = {'placeholder': item_to_update.past_price}
		form.current_price.render_kw = {'placeholder': item_to_update.current_price}
		form.category.render_kw = {'placeholder': item_to_update.category}
		form.product_pic.render_kw = {'placeholder': item_to_update.picture}
		form.in_stock.render_kw = {'placeholder': item_to_update.instock}
		form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

		# on clicking the update items button
		if form.validate_on_submit():
			# get all the data inputed into the form
			product_name = form.product_name.data
			previous_price = form.previous_price.data
			current_price = form.current_price.data
			category = form.category.data
			in_stock = form.in_stock.data
			flash_sale = form.flash_sale.data

			# product_pic = form.product_pic.data 	#get the picture
			file = form.product_pic.data 	#get the picture
			file_name = secure_filename(file.filename)	#set the filename without spaces
			file_path = f'./products/{file_name}'	#set the filepath to be without spaces
			# product_pic.save(file_path)		#save the filepath
			file.save(file_path)		#save the filepath

			try:
				# set values collected into the form to be values of updated product
				Product.query.filter_by(id=item_id).update(dict(name=product_name, 
					picture=file_path,
					current_price=current_price,
					past_price=previous_price,
					category=category,
					instock=in_stock,
					flash_sale=flash_sale))

				# save updated product to database
				db.session.commit()

				message = f'The {product_name} has been updated in the database succesfully!'
				flash(message, category='success')
				print('Product updated!')

				return redirect('/view-items')

			except Exception as e:
				print(e)
				print('something went wrong')

				message = f'The {product_name} has not been updated. Try again?'
				flash(message, category='danger')


		return render_template('update_items.html', form=form, user=current_user)

	return render_template('error_404.html', user=current_user)


@admin.route('delete-items/<int:item_id>', methods=['GET','POST'])
def delete_items(item_id):
	if current_user.id == 1:
		try:
			# get the insatnace of the item to delete in the db
			item_to_delete = Product.query.get(item_id)
			db.session.delete(item_to_delete)
			db.session.commit()

			message = 'The item has been successfuly deleted from the database'
			flash(message, category='success')

			return redirect('/view-items')

		except Exception as e:
			print(e)
			message = 'An error occured while trying to delete the item from the database. Try again?'
			flash(message, category='warning')

			return redirect('/view-items')

		return render_template('delete_items.html', form=form, user=current_user)


	return render_template('error_404.html', user=current_user)









