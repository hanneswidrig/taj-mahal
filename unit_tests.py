import unittest

from flask import g

import db
from app import app
import sys
import re
#from io import BytesIO


def getCSRF(resp):
	lines = resp.get_data(as_text=True).split("\n")
	csrf = ""
	for line in lines:
		match = re.match(r'.*id="csrf_token".*value="(.*)".*', line)
		if match is not None:
			csrf = match.group(1)
			break
	return csrf


class FlaskTestCase(unittest.TestCase):
	# This is a helper class that sets up the proper Flask execution context
	# so that the test cases that inherit it will work properly.
	def setUp(self):
		# Allow exceptions (if any) to propagate to the test client.
		app.testing = True

		# Create a test client.
		self.client = app.test_client(use_cookies=True)

		# Create an application context for testing.
		self.app_context = app.test_request_context()
		self.app_context.push()

	def tearDown(self):
		# Clean up the application context.
		self.app_context.pop()


class DatabaseTestCaseDay0(FlaskTestCase):
	"""Setup Cursor for Testing"""
	@staticmethod
	def execute_sql(resource_name):
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		super(DatabaseTestCaseDay0, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')

	def tearDown(self):
		db.close_db()
		super(DatabaseTestCaseDay0, self).tearDown()
	"""------------------------"""

	def test_all_listings(self):
		listings = db.all_listings()
		self.assertEqual(len(listings), 0, "All Listings Day 0 - Unexpected extra listings.")

	def test_all_users(self):
		users = db.all_users()
		self.assertEqual(len(users), 0, "All Users Day 0 - Unexpected extra users.")

	def test_title_like_listings(self):
		listings = db.title_like_listings("addtest")
		self.assertEqual(len(listings), 0, "Title Like Listings Day 0 - Unexpected match for listing.")

	def test_search_like_category(self):
		listings = db.search_like_category("veg")
		self.assertEqual(len(listings), 0, "Search Like Category Day 0 - Unexpected match for category.")

	def test_search_like_users(self):
		users = db.search_like_users("ha")
		self.assertEqual(len(users), 0, "Search Like Users Day 0 - Unexpected match for user.")

	def test_add_listing(self):
		try:
			rowcount = db.add_listing({
				'seller_id': 0,
				'title': "addtest",
				'photo': "",
				'description': "This is a test.",
				'original_quantity': 10,
				'available_quantity': 10,
				'unit_type': "each",
				'price_per_unit': 1.1,
				'total_price': 11.0,
				'category_id': 1,
				'date_harvested': "2018-04-19",
				'is_tradeable': True})
		except:
			self.assertTrue(True, "Add Listing Day 0 - This should pass. Listing should not be added without category.")
			return

		self.assertTrue(False, "Add Listing Day 0 - This should not be reached. Listing should not be added without category.")

	def test_get_one_listing(self):
		listing = db.get_one_listing(1)
		self.assertTrue(listing is None, "Get One Listing Day 0 - Non-existent listing should not have returned.")

	def test_get_one_user(self):
		user = db.get_one_user(1)
		self.assertTrue(user is None, "Get One User Day 0 - Non-existent listing should not have returned.")

	def test_get_one_login(self):
		user = db.get_one_login("jon@meharg.gov")
		self.assertTrue(user is None, "Get One Login Day 0 - Non-existent user should not have returned.")

	def test_get_user_listings(self):
		listings = db.get_user_listings(4)
		self.assertEqual(len(listings), 0, "Get User Listings Day 0 - Returned listings for non-existent user.")

	def test_update_available_quantity(self):
		rowcount = db.update_available_quantity(4, 1)
		self.assertEqual(rowcount, 0, "Update Available Quantity Day 0 - Update quantity affected unexpected row.")

	def test_get_user_address(self):
		address = db.get_user_address(2)
		self.assertTrue(address is None, "Get User Address Day 0 - Address returned for non-existent user.")

	def test_get_user_address_via_listing(self):
		address = db.get_user_address_via_listing(4)
		self.assertTrue(address is None, "Get User Address Via Listing Day 0 - Address returned for non-existent listing.")

	def test_get_listing_details_for_confirmation_page(self):
		details = db.get_listing_details_for_confirmation_page(4)
		self.assertTrue(details is None, "Get Listing Details For Confirmation Page Day 0 - Details returned for non-existent listing.")

	def test_add_new_order(self):
		try:
			rowcount = db.add_new_order(4, 7, 7.00, 2)
		except:
			self.assertTrue(True, "Add New Order Day 0 - This should pass. Listing does not exist.")
			return

		self.assertTrue(False, "Add New Order Day 0 - This should not be reached. Order added for non-existent listing.")

	def test_create_user(self):
		rowcount = db.create_user({
			"address_id": 1,
			"email": "brandongeorgeis@manly.com",
			"first": "brandon",
			"last": "george",
			"photo": 'images/uploaded-images/Corn.jpg',
			"pass": "somanly",
			"bio": "Oh man!"})
		self.assertEqual(rowcount, 1, "Create User Day 0 - Failed to create new user.")


class DatabaseTestCaseDay1(FlaskTestCase):
	"""Setup Cursor for Testing"""

	@staticmethod
	def execute_sql(resource_name):
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		super(DatabaseTestCaseDay1, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')
		self.execute_sql('db\seed_tables_day1.sql')

	def tearDown(self):
		db.close_db()
		super(DatabaseTestCaseDay1, self).tearDown()

	"""------------------------"""

	def test_all_listings(self):
		listings = db.all_listings()
		self.assertEqual(len(listings), 5, "All Listings Day 1 - Unexpected number of listings in day 1.")

	def test_all_users(self):
		users = db.all_users()
		self.assertEqual(len(users), 4, "All Users Day 1 - Unexpected number of users in day 1.")

	def test_title_like_listings(self):
		db.add_listing({
			'seller_id': 0,
			'title': "addtest1",
			'photo': "",
			'description': "This is a test.",
			'original_quantity': 10,
			'available_quantity': 10,
			'unit_type': "each",
			'price_per_unit': 1.1,
			'total_price': 11.0,
			'category_id': 1,
			'date_harvested': "2018-04-19",
			'is_tradeable': True})

		listings = db.title_like_listings("addtest")
		self.assertEqual(len(listings), 1, "Title Like Listings Day 1 - Unexpected number of listings like \"addtest\" in day 1.")

		db.add_listing({
			'seller_id': 0,
			'title': "addtest2",
			'photo': "",
			'description': "This is a test.",
			'original_quantity': 10,
			'available_quantity': 10,
			'unit_type': "each",
			'price_per_unit': 1.1,
			'total_price': 11.0,
			'category_id': 1,
			'date_harvested': "2018-04-19",
			'is_tradeable': True})

		listings = db.title_like_listings("addtest")
		self.assertEqual(len(listings), 2, "Title Like Listings Day 1 - Unexpected number of listings like \"addtest\" in day 1.")

	def test_search_like_category(self):
		listings = db.search_like_category("veg")
		self.assertEqual(len(listings), 5, "Search Like Category Day 1 - Unexpected number of listings in vegetable category.")

		listings = db.search_like_category("fru")
		self.assertEqual(len(listings), 0, "Search Like Category Day 1 - Unexpected number of listings in fruit category.")

	def test_search_like_users(self):
		users = db.search_like_users("ha")
		self.assertEqual(len(users), 2, "Search Like Users Day 1 - Unexpected number of users with \"ha\".")

		users = db.search_like_users("jon")
		self.assertEqual(len(users), 1, "Search Like Users Day 1 - Unexpected number of users with \"jon\".")

		users = db.search_like_users("john")
		self.assertEqual(len(users), 0, "Search Like Users Day 1 - Unexpected number of users with \"john\".")

	def test_add_listing(self):
		rowcount = db.add_listing({
			'seller_id': 0,
			'title': "addtest",
			'photo': "",
			'description': "This is a test.",
			'original_quantity': 10,
			'available_quantity': 10,
			'unit_type': "each",
			'price_per_unit': 1.1,
			'total_price': 11.0,
			'category_id': 1,
			'date_harvested': "2018-04-19",
			'is_tradeable': True})
		self.assertEqual(rowcount, 1, "Add Listing Day 1 - Adding listing failed.")

	def test_get_one_listing(self):
		listing = db.get_one_listing(1)
		self.assertEqual(listing['title'], "Peppers")

	def test_get_one_user(self):
		user = db.get_one_user(10)
		self.assertTrue(user is None, "Get One User Day 1 - Non-existent user should not have returned.")

		user = db.get_one_user(2)
		self.assertEqual(user["first_name"], "amish", "Get One User Day 1 - Unable to get user with id of 2.")

	def test_get_one_login(self):
		user = db.get_one_login("jon@meharg.gov")
		self.assertEqual(user["first_name"], "jon", "Get One Login Day 1 - Non-existent user should not have returned.")

	def test_get_user_listings(self):
		listings = db.get_user_listings(1)
		self.assertEqual(len(listings), 1, "Get User Listings Day 1 - Unexpected number of listings returned for user with id 1.")

		listings = db.get_user_listings(4)
		self.assertEqual(len(listings), 2, "Get User Listings Day 1 - Unexpected number of listings returned for user with id 4.")

	def test_update_available_quantity(self):
		rowcount = db.update_available_quantity(4, 10)
		self.assertEqual(rowcount, 0, "Update Available Quantity Day 1 - Updated non-existent listing available_quantity.")

		db.update_available_quantity(7, 1)
		listing = db.get_one_listing(1)
		self.assertEqual(listing["available_quantity"], 43, "Update Available Quantity Day 1 - Unexpected available quantity after update.")

	def test_get_user_address(self):
		address = db.get_user_address(2)
		self.assertEqual(address["street"], '236 West Reade Ave', "Get User Address Day 1 - Unexpected address returned for user with id 2.")

		address = db.get_user_address(10)
		self.assertTrue(address is None, "Get User Address Day 1 - Address returned for non-existent user.")

	def test_get_user_address_via_listing(self):
		address = db.get_user_address_via_listing(4)
		self.assertEqual(address["street"], "236 West Reade Ave", "Get User Address Via Listing Day 1 - Unexpected address returned for listing with id 4.")

		address = db.get_user_address_via_listing(10)
		self.assertTrue(address is None, "Get User Address Via Listing Day 1 - Address returned for non-existent listing.")

	def test_get_listing_details_for_confirmation_page(self):
		details = db.get_listing_details_for_confirmation_page(4)
		self.assertEqual(details["first_name"], "tim", "Get Listing Details For Confirmation Page Day 1 - Unexpected first name returned for listing details with id 4.")

		details = db.get_listing_details_for_confirmation_page(10)
		self.assertTrue(details is None, "Get Listing Details For Confirmation Page Day 1 - Details returned for non-existent listing.")

	def test_add_new_order(self):
		rowcount = db.add_new_order(4, 7, 7.00, 2)
		self.assertEqual(rowcount, 1, "Add New Order Day 1 - Failed to add order on listing with id 4.")

		try:
			rowcount = db.add_new_order(10, 7, 7.00, 2)
		except:
			self.assertTrue(True, "Add New Order Day 1 - This should pass. Listing does not exist.")
			return

		self.assertTrue(False, "Add New Order Day 1 - This should not be reached. Order added for non-existent listing.")


class ApplicationTestCaseDay0(FlaskTestCase):
	"""Setup Cursor for Testing"""
	@staticmethod
	def execute_sql(resource_name):
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		super(ApplicationTestCaseDay0, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')

	def tearDown(self):
		db.close_db()
		super(ApplicationTestCaseDay0, self).tearDown()
	"""------------------------"""

	def test_index(self):
		resp = self.client.get('/')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Index Day 0 - Missing site title.")
		self.assertTrue(b'Product Feed' in resp.data, "Index Day 0 - Missing page title.")
		self.assertTrue(b'No search results found' in resp.data, "Index Day 0 - Missing default response.")

	def test_listing_detail(self):
		try:
			resp = self.client.get('/listing/1')
		except:
			self.assertTrue(True, "Listing Detail Day 0 - This should pass. Listing does not exist.")
			return

		self.assertTrue(False, "Listing Detail Day 0 - This should not be reached. Listing does not exist.")

	def test_search(self):
		resp = self.client.get('/search')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 0 - Missing site title for no search.")
		self.assertTrue(b'Search for amazing products nearby!' in resp.data, "Search Day 0 - Found matches for no search.")

		resp = self.client.get('/search?search=thing')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 0 - Missing site title on bad search.")
		self.assertTrue(b'We could not find any matching products' in resp.data, "Search Day 0 - Found matches for bad search.")

	def test_listing_purchase(self):
		resp = self.client.get('/listing/buy/1', follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Purchase Day 0 - Missing site title.")
		self.assertTrue(b'Login' in resp.data, "Listing Purchase Day 0 - Missing login page title.")

	def test_new_listing(self):
		resp = self.client.get('/listing/add', follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Purchase Day 0 - Missing site title.")
		self.assertTrue(b'Login' in resp.data, "Listing Purchase Day 0 - Missing login page title.")

	def test_user_profile(self):
		try:
			resp = self.client.get('/user/1')
		except:
			self.assertTrue(True, "User Profile Day 0 - This should pass. User does not exist.")
			return

		self.assertTrue(False, "User Profile Day 0 - This should not be reached. User does not exist.")

	def test_account(self):
		resp = self.client.get('/account')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Account Day 0 - Missing site title.")
		self.assertTrue(b'Your Account' in resp.data, "Account Day 0 - Missing page title.")

	def test_settings(self):
		resp = self.client.get('/settings')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Settings Day 0 - Missing site title.")
		self.assertTrue(b'Settings' in resp.data, "Settings Day 0 - Missing page title.")

	def test_log_in(self):
		resp = self.client.get('/login')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Login Day 0 - Missing site title.")
		self.assertTrue(b'Password' in resp.data, "Login Day 0 - Missing title for password field.")


class ApplicationTestCaseDay1(FlaskTestCase):
	"""Setup Cursor for Testing"""

	@staticmethod
	def execute_sql(resource_name):
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		super(ApplicationTestCaseDay1, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')
		self.execute_sql('db\seed_tables_day1.sql')

	def tearDown(self):
		db.close_db()
		super(ApplicationTestCaseDay1, self).tearDown()

	"""------------------------"""

	def test_index(self):
		resp = self.client.get('/')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Index Day 1 - Missing site title.")
		self.assertTrue(b'Product Feed' in resp.data, "Index Day 1 - Missing page title.")
		self.assertTrue(b'Corn' in resp.data, "Index Day 1 - Missing tile for corn listing.")

	def test_listing_detail(self):
		resp = self.client.get('/listing/1')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Detail Day 1 - Missing site title.")
		self.assertTrue(b'Peppers' in resp.data, "Listing Detail Day 1 - Missing listing title.")
		self.assertTrue(b'1.00' in resp.data, "Listing Detail Day 1 - Missing price per unit.")

	def test_search(self):
		resp = self.client.get('/search')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 1 - Missing site title for no search.")
		self.assertTrue(b'Search for amazing products nearby!' in resp.data, "Search Day 1 - Found matches for no search.")

		resp = self.client.get('/search?search=thing')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 1 - Missing site title on bad search.")
		self.assertTrue(b'We could not find any matching products' in resp.data, "Search Day 1 - Found matches for bad search.")

		resp = self.client.get('/search?search=i')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 1 - Missing site title on broad search.")
		self.assertTrue(b'Zucchini' in resp.data, "Search Day 1 - Missing listing match for broad search.")
		self.assertTrue(b'Amish' in resp.data, "Search Day 1 - Missing user match for broad search.")

	def test_listing_purchase(self):
		resp = self.client.get('/listing/buy/1', follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Purchase Day 1 - Missing site title.")
		self.assertTrue(b'Login' in resp.data, "Listing Purchase Day 1 - Missing login page title.")

		resp = self.client.get('/login')
		csrf = getCSRF(resp)
		resp = self.client.post("/login", data=dict(csrf_token=csrf, email="tim@ours.org", password="tim"),
		                        follow_redirects=True)

		resp = self.client.get('/listing/buy/1')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Purchase Day 1 1 - Missing site title.")
		self.assertTrue(b'Quantity Available' in resp.data, "Listing Purchase Day 1 1 - Missing available quantity.")
		self.assertTrue(b'50' in resp.data, "Listing Purchase Day 1 1 - Unexpected available quantity before update.")

		csrf = getCSRF(resp)
		resp = self.client.post("/listing/buy/1", data=dict(csrf_token=csrf, quantity=7, submit="Pay"), follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Purchase Day 1 2 - Missing site title.")
		self.assertTrue(b'Total' in resp.data, "Listing Purchase Day 1 2 - Missing title for total.")
		self.assertTrue(b'7.00' in resp.data, "Listing Purchase Day 1 2 - Unexpected total.")

		resp = self.client.get('/listing/buy/1')
		csrf = getCSRF(resp)
		resp = self.client.post("/listing/buy/1", data=dict(csrf_token=csrf, quantity=60, submit="Make+Purchase"), follow_redirects=True)
		self.assertTrue(b'Pay' in resp.data, "Listing Purchase Day 1 2 - Should still be on buy listing page.")
		self.assertTrue(b'Please select no more than the quantity that is available.' in resp.data, "Listing Purchase Day 1 2 - Missing flash message when purchase too large.")
		self.assertTrue(b'Quantity Available' in resp.data, "Listing Purchase Day 1 2 - Did not find quantity available on buy listing page.")
		self.assertTrue(b'43' in resp.data, "Listing Purchase Day 1     2 - Did not find expected available quantity on buy listing page.")

		try:
			resp = self.client.get('/listing/buy/10')
		except:
			self.assertTrue(True, "Buy Listing Day 1 - This should pass. Listing does not exist.")
			return

		self.assertTrue(False, "Buy Listing Day 1 - This should not be reached. Listing does not exist.")

	def test_new_listing(self):
		resp = self.client.get('/listing/add', follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Listing Purchase Day 1 - Missing site title.")
		self.assertTrue(b'Login' in resp.data, "Listing Purchase Day 1 - Missing login page title.")

		resp = self.client.get('/login')
		csrf = getCSRF(resp)
		resp = self.client.post("/login", data=dict(csrf_token=csrf, email="tim@ours.org", password="tim"),
		                        follow_redirects=True)

		resp = self.client.get('/listing/add')
		# csrf = getCSRF(resp)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "New Listing Day 1 - Missing site title.")
		self.assertTrue(b'Title' in resp.data, "New Listing Day 1 - Missing title field.")

		# f = open("./static/images/uploaded-images/Corn.jpg", "rb")
		# read_data = f.read()
		#
		# resp = self.client.post("/listing/add", data=dict(csrf_token=csrf, title="test", photo=(bytes(read_data), "image.jpg"),
		#                                                     description="This is a test.", original_quantity=10,
		#                                                     unit_type="each", price_per_unit=0.97,
		#                                                     category_id=1, is_tradeable="y",
		#                                                     date_harvested="2018-05-02", submit="Add"),
		#                         follow_redirects=True)
		#
		# f.close()
		#
		# text = resp.get_data(as_text=True).split("\n")
		# for i in text:
		# 	print(i, file=sys.stderr)
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "New Listing Day 1 - Missing site title.")
		# self.assertTrue(b'Product Feed' in resp.data, "New Listing Day 1 - Missing page title.")
		# self.assertTrue(b'vegetable' in resp.data, "Did not find expected category on add listing page.")

	def test_user_profile(self):
		resp = self.client.get('/user/1')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "User Profile Day 1 - Missing site title.")
		self.assertTrue(b'Hannes' in resp.data, "User Profile Day 1 - Missing first name.")
		self.assertTrue(b'Peppers' in resp.data, "User Profile Day 1 - Missing listing title.")

		try:
			resp = self.client.get("/user/10")
		except:
			self.assertTrue(True, "User Profile Day 1 - This should pass. User does not exist.")
			return

		self.assertTrue(False, "User Profile Day 1 - This should not be reached. User does not exist.")

	def test_log_in(self):
		resp = self.client.get('/login')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Login Day 1 - Missing site title.")
		self.assertTrue(b'Password' in resp.data, "Login Day 1 - Missing title for password field.")

		csrf = getCSRF(resp)
		resp = self.client.post("/login", data=dict(csrf_token=csrf, email="tim@ours", password="tim"), follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Login Day 1 - Missing site title.")
		self.assertTrue(b'Invalid email' in resp.data, "Login Day 1 - Missing invalid email in flash.")

		resp = self.client.get('/login')
		csrf = getCSRF(resp)
		resp = self.client.post("/login", data=dict(csrf_token=csrf, email="tim@ours.org", password="nottim"), follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Login Day 1 - Missing site title.")
		self.assertTrue(b'Invalid password' in resp.data, "Login Day 1 - Missing invalid password in flash.")

		resp = self.client.get('/login')
		csrf = getCSRF(resp)
		resp = self.client.post("/login", data=dict(csrf_token=csrf, email="tim@ours.org", password="tim"), follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Login Day 1 - Missing site title.")
		self.assertTrue(b'logged in' in resp.data, "Login Day 1 - Missing logged in flash.")

	def test_logout(self):
		resp = self.client.get('/login')
		csrf = getCSRF(resp)
		self.client.post('/login', data=dict(csrf_token=csrf, email="tim@ours.org", password="tim"), follow_redirects=True)

		resp = self.client.get('/logout', follow_redirects=True)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Logout Day 1 - Missing site title.")
		self.assertTrue(b'logged out' in resp.data, "Logout Day 1 - Missing logged out flash.")


if __name__ == '__main__':
	unittest.main()
