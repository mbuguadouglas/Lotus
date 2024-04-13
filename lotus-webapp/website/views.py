from flask import Flask, Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import Product, Customer, Cart


views = Blueprint('views',__name__)



@views.route('/',methods=['GET','POST'])
@login_required
def index():

	items = Product.query.filter_by(flash_sale=True)
	cart_items = Cart.query.filter_by(customer_id=current_user.id).all()

	return render_template('index.html', user=current_user, items=items, cart=cart_items
	if current_user.is_authenticated else [])


@views.route('/add-to-cart/<int:item_id>',methods=['GET','POST'])
def add_to_cart(item_id):

	item_to_add = Product.query.get(item_id)

	# check if the item already exists in the cart
	item_exists = Cart.query.filter_by(product_id=item_id, customer_id=current_user.id).first()

	# if it does exist increment its value by one
	if item_exists:
		try:
			item_exists.items += 1		#increment value by 1
			db.session.commit()

			# link used for Product table MUST BE HOW YOU NAMED YOUR TABLES USING __tablename__
			message = f'Quantity of {item_exists.products.name} has been updated'
			flash(message, category='success')

			return redirect(request.referrer)	#will redirect you back to the home page

		except Exception as e:
			print(e)
			# link used for Product table MUST BE HOW YOU NAMED YOUR TABLES USING __tablename__
			message = f'Quantity of {item_exists.products.name} has not been updated'
			flash(message, category='success')

			return redirect(request.referrer)	#will redirect you back to the home page(initial page you were in)

	# else you create and add new item
	print('creating new item')
	new_cart_item = Cart(items=1, product_id=item_to_add.id,customer_id=current_user.id)
	try:
		db.session.add(new_cart_item)
		db.session.commit()

		# link used for Product table MUST BE HOW YOU NAMED YOUR TABLES USING __tablename__
		message = f'The {new_cart_item.products.name } was succesfuly added to the cart!'
		flash(message, category='info')

	except Exception as e:
		print(e)
		# link used for Product table MUST BE HOW YOU NAMED YOUR TABLES USING __tablename__
		message = f'The {new_cart_item.products.name} item was not added to the cart. Try again?'

		flash(message, category='warning')

	return redirect(request.referrer)	#will redirect you back to the home page(initial page you were in)



@views.route('/view-cart/<int:customers_id>',methods=['GET','POST'])
def view_cart(customers_id):

	cart = Cart.query.filter_by(customer_id = current_user.id).all()
	amount = 0
	shipping_fee = 200

	for item in cart:
		amount += item.products.current_price * item.items

	return render_template('view_cart.html', user=current_user,
		cart=cart,
		amount=amount,
		total=amount+shipping_fee )
