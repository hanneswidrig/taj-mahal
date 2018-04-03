# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import Email, Length, DataRequired, Regexp, NumberRange

import sys

# Imported Project Files
import db
from secrets import secret_flask_key

app = Flask('Gardener\'s Exchange')
app.config['SECRET_KEY'] = secret_flask_key()

@app.before_request
def before_request():
	db.open_db()

def after_request():
	db.close_db()

@app.route('/')
def index():
	listings = db.all_listings()
	for listing in listings:
		listing['price_per_unit'] = '${:,.2f}'.format(listing['price_per_unit'])
	return render_template('index.html', listings=listings)

@app.route('/listing/<int:id>')
def listing_detail(id):
	listing = db.get_one_listing(id)
	return render_template('detail-listing.html', listing=listing)

class BuyForm(FlaskForm):
    quantity = DecimalField('Quantity to buy', validators=[NumberRange(min=0.001, message="Must buy more than 0.")])
    submit = SubmitField('Make Purchase')

@app.route('/listing/buy/<int:id>', methods=['GET', 'POST'])
def buy_listing(id):
	listing = db.get_one_listing(id)
	buy_item = BuyForm()
	if (buy_item.validate_on_submit() and buy_item.quantity.data <= listing['available_quantity']
		and buy_item.quantity.data > 0):
		pass
		#TODO: update database with new quantity remaining
	elif (buy_item.validate_on_submit() and buy_item.quantity.data > listing['available_quantity']):
		flash("Please select no more than the quantity that is available.")
	else:
		flash("Unable to purchase item")
	return render_template('buy_listing.html', listing=listing, form=buy_item)

@app.route('/listing/add')
def listing_add(id):
	# Will need to be modified when we are implementing back button for purchasing
	# and other secured navigation.
	rel_link = request.referrer
	if rel_link is None:
		rel_link = '/'
	listing  = db.get_one_listing(id)
	return render_template('detail-listing.html', listing=listing, rel_link=rel_link)

@app.route('/listing/add', methods=["GET", "POST"])
def all_listings():
	return render_template('add-listing.html')

@app.route('/user')
def all_users():
	return '<h1>All Users</h1>'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
	return 'User ID: {0}'.format(user_id)

app.run(host='localhost', port=5000, debug=True)