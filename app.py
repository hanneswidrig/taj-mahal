# Pip Dependencies
from flask import Flask, render_template, request, flash, redirect, url_for
from PIL import Image
import pendulum

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
		results = {'listings': [], 'categories': [], 'users': []}
		c_flag = False

		if q is not None:
				results = route_functions.search(results, q)
		else:
				q = ''

		if filter_value is not None:
				results, c_flag = route_functions.filter(results, int(filter_value), q)

		return render_template('search.html', results=results, q=q, c_flag=c_flag)


@app.route('/listing/<int:id>')
def listing_detail(id):
		listing = db.get_one_listing(id)
		user = db.get_one_user(listing['seller_id'])
		rel_link = helper_functions.relative_link(request.path, request.referrer)
		return render_template('listing-detail.html', listing=listing, user=user, rel_link=rel_link)


@app.route('/listing/buy/<int:id>', methods=['GET', 'POST'])
def listing_purchase(id):
		listing = db.get_one_listing(id)
		buy_item = buy_form()
		rel_link = helper_functions.relative_link(request.path, request.referrer)

		if buy_item.validate_on_submit() and buy_item.quantity.data <= listing['available_quantity']:
				db.update_available_quantity(buy_item.quantity.data, id)
				return redirect(url_for('listing_detail', id=id))
		elif buy_item.validate_on_submit() and buy_item.quantity.data > listing['available_quantity']:
				flash('Please select no more than the quantity that is available.')
		elif buy_item.validate_on_submit():
				flash('Unable to purchase item')

		return render_template('listing-purchase.html', listing=listing, form=buy_item, rel_link=rel_link)


@app.route('/listing/add', methods=['GET', 'POST'])
def listing_new():
		listing_form = add_listing_form()
		rel_link = helper_functions.relative_link(request.path, request.referrer)
		if request.method == 'POST':
				if listing_form.submit.data and listing_form.validate_on_submit():
						seller_id = 1

						# Upload seller's photo
						approved_file_extensions = {'jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp'}
						file_name = secure_filename(listing_form.photo.data.filename)
						file_extension = file_name.split('.')[-1]

						if file_extension in approved_file_extensions:
							seller_dir = './static/images/uploaded-images/{}'.format(seller_id)
							if not os.path.exists(seller_dir):
								os.mkdir(seller_dir)
							file_path = os.path.join('images/uploaded-images/{}/'.format(seller_id), file_name)
							listing_form.photo.data.save('static/' + file_path)

							# Generate new filename to prevent overwrites
							current_time = pendulum.now('America/Indianapolis').format(r'%Y%m%dT%H%M%S')
							proc_name = '{}.{}'.format(current_time, file_extension)
							os.chdir('./static/images/uploaded-images/{}/'.format(seller_id))
							os.rename(file_name, proc_name)
							pic_location = 'images/uploaded-images/{}/{}'.format(seller_id, proc_name)

							# Resize photo to width < 1024 and compress file size
							img = Image.open(proc_name)
							maxsize = (1024, 1024)
							img.thumbnail(maxsize, Image.ANTIALIAS)
							img.save(proc_name, optimize=True, quality=50)

							# Properly calculate monetary values
							ppu = float(format(float(listing_form.price_per_unit.data), '.2f'))
							ogq = float(format(float(listing_form.original_quantity.data), '.2f'))
							total_price = float(format(ppu * ogq, '.2f'))
							category_id = int(listing_form.category_id.data)

							rowcount = db.add_listing({
									'seller_id': seller_id,
									'title': listing_form.title.data,
									'photo': pic_location,
									'description': listing_form.description.data,
									'original_quantity': int(listing_form.original_quantity.data),
									'available_quantity': int(listing_form.original_quantity.data),
									'unit_type': listing_form.unit_type.data,
									'price_per_unit': ppu,
									'total_price': total_price,
									'category_id': category_id,
									'date_harvested': listing_form.date_harvested.data,
									'is_tradeable': listing_form.is_tradeable.data})

							if rowcount == 1:
									flash('New listing for {0} created.'.format(listing_form.title.data))
									return redirect(url_for('index'))
							else:
									flash('New listing not created.')
						else:
							flash('Invalid image file format, please use PNG, JPG, or JPEG.')

		return render_template('listing-new.html', form=listing_form, rel_link=rel_link)


@app.route('/account')
def account():
		return render_template('account.html')


@app.route('/settings')
def settings():
		return render_template('settings.html')


@app.route('/user/<int:user_id>')
def user_profile(user_id):
		return 'User ID: {0}'.format(user_id)


if __name__ == '__main__':
		app.run(host='localhost', port=5000, debug=True)
