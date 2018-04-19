# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for, session

# Imported Project Files
import db
import os
import helper_functions
import route_functions
from form_classes import buy_form, add_listing_form
from secrets import secret_flask_key
from werkzeug.utils import secure_filename

app = Flask('Gardener\'s Exchange')
app.config['SECRET_KEY'] = secret_flask_key()
app.config['UPLOAD_FOLDER'] = 'images/uploaded-images/'

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


@app.route('/search')
def search():
		q = request.args.get('search')
		filter_value = request.args.get('filter')
		results = {'listings': [],'categories': [], 'users': []}

		if q is not None:
			results = route_functions.search(results, q)
		else:
			q = ''

		if filter_value is not None:
			results = route_functions.filter(results, int(filter_value), q)

		return render_template('search.html',results=results,search_query=q)


@app.route('/listing/<int:id>')
def listing_detail(id):
		listing = db.get_one_listing(id)
		user = db.get_one_user(listing['seller_id'])
		rel_link = helper_functions.relative_link(request.path, request.referrer)
		return render_template('detail-listing.html', listing=listing, user=user, rel_link=rel_link)


@app.route('/listing/buy/<int:id>', methods=['GET', 'POST'])
def buy_listing(id):
		listing = db.get_one_listing(id)
		buy_item = buy_form()
		rel_link = helper_functions.relative_link(request.path, request.referrer)

		if (buy_item.validate_on_submit() and buy_item.quantity.data <= listing['available_quantity']):
				db.update_available_quantity(buy_item.quantity.data, id)
				return redirect(url_for('listing_detail', id=id))
		elif (buy_item.validate_on_submit() and buy_item.quantity.data > listing['available_quantity']):
				flash("Please select no more than the quantity that is available.")
		elif (buy_item.validate_on_submit()):
				flash("Unable to purchase item")

		return render_template('buy-listing.html', listing=listing, form=buy_item, rel_link=rel_link)


@app.route('/listing/add', methods=['GET', 'POST'])
def new_listing():
		listing_form = add_listing_form()
		rel_link = helper_functions.relative_link(request.path, request.referrer)
		if listing_form.submit.data and listing_form.validate_on_submit():
			filename = secure_filename(listing_form.photo.data.filename)
			file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			listing_form.photo.data.save('static/' + file_path)

			rowcount = db.add_listing({
					'seller_id': 0,  # CHANGE TO GRAB ACTUAL ID AT LATER TIME
					'title': listing_form.title.data,
					'photo': file_path,
					'description': listing_form.description.data,
					'original_quantity': listing_form.original_quantity.data,
					'available_quantity': listing_form.original_quantity.data,
					'unit_type': listing_form.unit_type.data,
					'total_price': listing_form.price_per_unit.data*listing_form.original_quantity.data,
					'price_per_unit': listing_form.price_per_unit.data,
					'listing_category': listing_form.listing_category.data,
					'date_harvested': listing_form.date_harvested.data,
					'is_tradeable': listing_form.is_tradeable.data})

			if rowcount == 1:
				#flash("New listing for {} created.".format(listing_form.title.data))
				return redirect(url_for('index'))
			#else:
				#flash("New listing not created.")

		return render_template('add-listing.html', form=listing_form, rel_link=rel_link)


@app.route('/user')
def all_users():
		return '<h1>All Users</h1>'


@app.route('/user/<int:user_id>')
def user_profile(user_id):
		return 'User ID: {0}'.format(user_id)

if __name__ == '__main__':
	app.run(host='localhost', port=5000, debug=True)