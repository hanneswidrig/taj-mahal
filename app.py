# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import Email, Length, DataRequired, Regexp

import sys

# Imported Project Files
import db
import helper_functions
from secrets import secret_flask_key

app = Flask('Gardener\'s Exchange')
app.config['SECRET_KEY']  = secret_flask_key()


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
	listing         = db.get_one_listing(id)
	rel_link        = helper_functions.relative_link(request.referrer)
	return render_template('detail-listing.html', listing=listing, rel_link=rel_link)


class BuyForm(FlaskForm):
    quantity = DecimalField('Quantity to buy')
    submit = SubmitField('Make Purchase')


@app.route('/listing/buy/<int:id>', methods=['GET', 'POST'])
def buy_listing(id):
	listing = db.get_one_listing(id)
	buy_item = BuyForm()
	rel_link = helper_functions.relative_link(request.referrer)

	if (buy_item.validate_on_submit() and buy_item.quantity.data <= listing['available_quantity']):
		pass
		#TODO: update database with new quantity remaining
	else:
		flash("Unable to purchase item")

	return render_template('buy-listing.html', listing=listing, form=buy_item, rel_link=rel_link)


@app.route('/listing/add', methods=["GET", "POST"])
def add_listing():
	rel_link = helper_functions.relative_link(request.referrer)
	return render_template('add-listing.html', rel_link=rel_link)


@app.route('/user')
def all_users():
	return '<h1>All Users</h1>'


@app.route('/user/<int:user_id>')
def user_profile(user_id):
	return 'User ID: {0}'.format(user_id)

app.run(host='localhost', port=5000, debug=True)