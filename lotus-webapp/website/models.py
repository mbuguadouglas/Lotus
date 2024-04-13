from . import db 
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# customer table for all the customers
class Customer(db.Model, UserMixin):
	__tablename__ = 'customers'

	id = db.Column(db.Integer, primary_key=True, index=True)
	email = db.Column(db.String(50), unique=True , nullable=False)
	name = db.Column(db.String(50))
	# password_hash = db.Column(db.String(50))
	password = db.Column(db.String(50))
	date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

	# setup foreign keys
	order_item = db.Relationship('Order', backref=db.backref('customers'))	# 1.link customer to order
	cart_item = db.Relationship('Cart', backref=db.backref('customers'))		# 2.link customer to cart
	# product = db.Relationship('Product', backref=db.backref('customer'))		# 3.link customer to product table

	#################################################
	######did not work as required###################
	######when called in auth.py kepr returning #####
	######create new acc yet passwords match#########
	#################################################
	
	# use getter and setter methods to set password hash and allow for its retrieval
	# @property
	# def password(self):
	# 	raise AttributeError('Password is not readable')
	
	# # setter
	# @password.setter
	# def password(self, password):
	# 	self.password_hash = generate_password_hash(password=password)

	# # password verification
	# def verify_password(self,password):
	# 	# if passwords match(correct) return true, else return false
	# 	return check_password_hash(self.password_hash, password=password)

	# string method to allow for better represenattion of class
	def __str__(self):
		#string formatiing. see if you can use f Strings
		#f'<Customer {Customer.id}' 
		return '<Customer %r >' % Customer.id


# product table for all the shop items
class Product(db.Model):
	__tablename__ = 'products'

	id = db.Column(db.Integer, primary_key=True, index=True)
	name = db.Column(db.String(50), nullable=False)
	picture = db.Column(db.String(1000))	#why is the picture set as a string?! #only storethe path to pic!!
	category = db.Column(db.String(50))
	current_price = db.Column(db.Float(), nullable=False)
	past_price = db.Column(db.Float(), nullable=False)
	instock = db.Column(db.Integer())
	flash_sale = db.Column(db.Boolean, default=False)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)


	# setup and foreign key with cart & order table
	cart_id = db.Relationship('Cart', backref=db.backref('products'))
	order_id = db.Relationship('Order', backref=db.backref('products'))

	# __str__ method to return human redable form of product
	def __str__(self):
		# are fStrings possible?
		return '<Product %r>' % self.name

class Cart(db.Model):
	__tablename__ = 'carts'

	id = db.Column(db.Integer, primary_key=True)
	items = db.Column(db.Integer, nullable=False)

	# setup foreigh keys
	# should have called these link instead. easier to understand.
	customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

	def __str__(self):
		# return f'<Cart{self.id}'
		return '<Cart %r>' % self.id

class Order(db.Model):
	__tablename__ = 'orders'

	id = db.Column(db.Integer, primary_key=True)
	items = db.Column(db.Integer, nullable=False)
	price = db.Column(db.Float, nullable=False)
	status = db.Column(db.String, nullable=False)
	payment_id = db.Column(db.String(1000))

	# setup foreign key
	product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
	customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

	def __str__(self):
		# return f'Order {self.name}'
		return '<Order %r>' % self.name



