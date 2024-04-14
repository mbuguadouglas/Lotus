from flask import Flask, Blueprint, render_template, redirect, flash, url_for, request, jsonify
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



@views.route('/view-cart',methods=['GET','POST'])
def view_cart():
	cart = Cart.query.filter_by(customer_id = current_user.id).all()
	amount = 0
	shipping_fee = 200

	for item in cart:
		amount += item.products.current_price * item.items

	return render_template('view_cart.html', user=current_user, cart=cart,
		amount=amount,
		total=amount+shipping_fee )




@views.route('/plus-cart', methods=['GET','POST'])
@login_required
def plus_cart():
	# get the cart id from the ajax request
	if request.method == 'GET':
		cart_id = request.args.get('cart_id')
		cart_item = Cart.query.get(cart_id)
		# cart_item.items = cart_item.items + 1
		cart_item.items += 1
		db.session.commit()

		# update values of items in db
		cart = Cart.query.filter_by(customer_id=current_user.id).all()
		amount = 0
		for item in cart:
			amount = item.products.current_price * current_price

		shipping_fee = 200
		total_amount = amount + shipping_fee

		# send out a response
		data = {
			'quantity' : cart_item.items,
			'amount' : amount,
			'total' : total_amount
		}

	return jsonify(data)



@views.route('/minus-cart', methods=['GET','POST'])
@login_required
def minus_cart():
	# get the cart id from the ajax request
	if request.method == 'GET':
		cart_id = request.args.get('cart_id')
		cart_item = Cart.query.get(cart_id)
		# cart_item.items = cart_item.items - 1
		cart_item.items -= 1
		db.session.commit()

		# update values of items in db
		cart = Cart.query.filter_by(customer_id=current_user.id).all()
		amount = 0
		for item in cart:
			amount = item.products.current_price * current_price

		shipping_fee = 200
		total_amount = amount + shipping_fee

		# send out a response
		data = {
			'quantity' : cart_item.items,
			'amount' : amount,
			'total' : total_amount
		}

	return jsonify(data)
