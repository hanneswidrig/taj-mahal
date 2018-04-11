# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import Email, Length, DataRequired, Regexp, NumberRange

import sys
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, DecimalField, SelectField, BooleanField, DateField, \
    SubmitField
from wtforms.validators import Length, NumberRange

# Imported Project Files
import db
import helper_functions
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
        listing['price_per_unit'] = '${:,.2f}'.format(
            listing['price_per_unit'])
    return render_template('index.html', listings=listings)


@app.route('/search')
def search():
    search_query = request.args.get('search')
    listings = []
    if search_query is not None:
        listings = db.title_like_listings(search_query)
    else:
        search_query = ''
    return render_template('search.html', listings=listings, search_query=search_query)


@app.route('/listing/<int:id>')
def listing_detail(id):
    listing = db.get_one_listing(id)
    rel_link = helper_functions.relative_link(request.path)
    return render_template('detail-listing.html', listing=listing, rel_link=rel_link)


class BuyForm(FlaskForm):
    quantity = IntegerField('Quantity to buy', validators=[
                            NumberRange(min=0.01, message="Must buy more than 0.")])
    submit = SubmitField('Make Purchase')


@app.route('/listing/buy/<int:id>', methods=['GET', 'POST'])
def buy_listing(id):
    listing = db.get_one_listing(id)
    buy_item = BuyForm()
    rel_link = helper_functions.relative_link(request.path)

    if (buy_item.validate_on_submit() and buy_item.quantity.data <= listing['available_quantity']):
        db.update_available_quantity(buy_item.quantity.data, id)
        return redirect(url_for('listing_detail', id=id))
    elif (buy_item.validate_on_submit() and buy_item.quantity.data > listing['available_quantity']):
        flash("Please select no more than the quantity that is available.")
    elif (buy_item.validate_on_submit()):
        flash("Unable to purchase item")

    return render_template('buy-listing.html', listing=listing, form=buy_item, rel_link=rel_link)


class add_listing_form(FlaskForm):
    title = StringField('Title', validators=[Length(
        min=1, message="A title is required.")])
    photo = FileField('Picture')
    description = StringField('Description', validators=[
                              Length(min=1, message="A description is required.")])
    original_quantity = IntegerField(
        'Quantity', validators=[NumberRange(min=1, message="A quantity is required.")])
    unit_type = StringField('Measurement', validators=[
                            Length(min=1, message="A measurement is required.")])
    price_per_unit = DecimalField('Price Per Unit', places=2,
                                  validators=[NumberRange(min=1, message="A price is required.")])
    listing_category = SelectField('Category',
                                   choices=[('vegetable', 'Vegetable'), ('fruit', 'Fruit'), ('other', 'Other')])
    listing_quality = SelectField('Quality', choices=[(
        'fresh', 'Fresh'), ('not fresh', 'Not Fresh')])
    is_tradeable = BooleanField('Tradeable')
    expiration_date = DateField('Expiration Date', format="%Y-%m-%d")
    submit = SubmitField('Add')


@app.route('/listing/add', methods=['GET', 'POST'])
def new_listing():
    listing_form = add_listing_form()
    rel_link = helper_functions.relative_link(request.path)
    if listing_form.submit.data and listing_form.validate_on_submit():
        rowcount = db.add_listing({
            'seller_id': 0,  # CHANGE TO GRAB ACTUAL ID AT LATER TIME
            'title': listing_form.title.data,
            'photo': listing_form.photo.data,
            'description': listing_form.description.data,
            'original_quantity': listing_form.original_quantity.data,
            'unit_type': listing_form.unit_type.data,
            'price_per_unit': listing_form.price_per_unit.data,
            'listing_category': listing_form.listing_category.data,
            'listing_quality': listing_form.listing_quality.data,
            'is_tradeable': listing_form.is_tradeable.data,
            'expiration_date': listing_form.expiration_date.data})

        if rowcount == 1:
            flash("New listing for {} created.".format(listing_form.title.data))
            return redirect(url_for('index'))
        else:
            flash("New listing not created.")

    return render_template('add-listing.html', form=listing_form, rel_link=rel_link)


@app.route('/user')
def all_users():
    return '<h1>All Users</h1>'


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return 'User ID: {0}'.format(user_id)


app.run(host='localhost', port=5000, debug=True)
