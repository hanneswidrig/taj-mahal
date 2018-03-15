# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
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

@app.route('/listing')
def listing_add():
	listings = db.all_listings()
	return render_template('all-listings.html', listings=listings)

@app.route('/listing/<int:id>')
def listing_detail(id):
	return render_template('detail-listing.html', id=id)

@app.route('/listing/add')
def all_listings():
	return render_template('add-listing.html')

@app.route('/user')
def all_users():
	return '<h1>All Users</h1>'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
	return 'User ID: {0}'.format(user_id)

app.run(host='0.0.0.0', port=8080, debug=True)