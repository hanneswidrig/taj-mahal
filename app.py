# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, DecimalField, SelectField, BooleanField, DateField, SubmitField
from wtforms.validators import Length, NumberRange

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
	return render_template('detail-listing.html', id=id)

class add_listing_form(FlaskForm):
	title             = StringField('Title', validators=[Length(min=1, message="A title is required.")])
	photo             = FileField('Picture')
	description       = StringField('Description', validators=[Length(min=1, message="A description is required.")])
	original_quantity = IntegerField('Quantity', validators=[NumberRange(min=1, message="A quantity is required.")])
	unit_type         = StringField('Measurement', validators=[Length(min=1, message="A measurement is required.")])
	price_per_unit    = DecimalField('Price Per Unit', places=2, validators=[NumberRange(min=1, message="A price is required.")])
	listing_category  = SelectField('Category', choices=[('vegetable', 'Vegetable'), ('fruit', 'Fruit'), ('other', 'Other')])
	listing_quality   = SelectField('Quality', choices=[('fresh', 'Fresh'), ('not fresh', 'Not Fresh')])
	is_tradeable      = BooleanField('Tradeable')
	expiration_date   = DateField('Expiration Date', format="%Y-%m-%d")
	submit            = SubmitField('Add')

@app.route('/listing/add', methods=['GET', 'POST'])
def all_listings():
	listing_form = add_listing_form()
	if listing_form.submit.data and listing_form.validate_on_submit():
		rowcount = db.add_listing(0, listing_form.title.data, '', listing_form.description.data, listing_form.original_quantity.data, listing_form.unit_type.data, listing_form.price_per_unit.data, listing_form.listing_category.data, listing_form.listing_quality.data, listing_form.is_tradeable.data, listing_form.expiration_date.data)

		if rowcount == 1:
			flash("New listing for {} created.".format(listing_form.title.data))
			return redirect(url_for('index'))
		else:
			flash("New listing not created.");
	return render_template('add-listing.html', form=listing_form)

@app.route('/user')
def all_users():
	return '<h1>All Users</h1>'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
	return 'User ID: {0}'.format(user_id)

app.run(host='localhost', port=5000, debug=True)