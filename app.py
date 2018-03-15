# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
import sys

# Imported Project Files
import db
import secrets

app = Flask('Gardener\'s Exchange')
app.config['SECRET_KEY'] = secrets.secret_flask_key()

@app.before_request
def before_request():
  pass # db.open_db()

def after_request():
  pass # db.close_db()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/listing')
def add_listing():
	return render_template('all-listings.html')

@app.route('/listing/add')
def all_listings():
	return render_template('add-listing.html')

@app.route('/user')
def all_users():
	return '<h1>All Users</h1>'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
	return 'User ID: {0}'.format(user_id)
	# return render_template('user-profile.html')

app.run(host='0.0.0.0', port=8080, debug=True)