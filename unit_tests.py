import unittest

from flask import g

import db
from app import app
import sys
import re


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
			row_count = db.add_listing({
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
			self.assertTrue(False, "Add Listing Day 0 - This should not be reached. Listing should not be added without category.")
		except:
			self.assertTrue(True, "Add Listing Day 0 - This should pass. Listing should not be added without category.")

	def test_get_one_listing(self):
		self.assertTrue(False, "Finish this test.")

	def test_get_one_user(self):
		try:
			user = db.get_one_user(1)
			self.assertTrue(False, "Get One User Day 0 - This should not be reached. User does not exist.")
		except:
			self.assertTrue(True, "Get One User Day 0 - This should pass. User does not exist.")

	def test_update_available_quantity(self):
		try:
			db.update_available_quantity(4, 1)
			self.assertTrue(False, "Update Available Quantity Day 0 - This should not be reached. Listing does not exist.")
		except:
			self.assertTrue(True, "Get One User Day 0 - This should pass. Listing does not exist.")


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
		row_count = db.add_listing({
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
		self.assertEqual(row_count, 1, "Add Listing Day 1 - Adding listing failed.")

	def test_get_one_listing(self):
		self.assertTrue(False, "Finish this test.")

	def test_get_one_user(self):
		try:
			user = db.get_one_user(10)
			self.assertTrue(False, "Get One User Day 1 - This should not be reached. User does not exist.")
		except:
			self.assertTrue(True, "Get One User Day 1 - This should pass. User does not exist.")

		user = db.get_one_user(2)
		self.assertEqual(user["first_name"], "amish", "Get One User Day 1 - Unable to get user with id of 2.")

	def test_update_available_quantity(self):
		try:
			db.update_available_quantity(4, 10)
			self.assertTrue(False, "Update Available Quantity Day 1 - This should not be reached. Listing does not exist.")
		except:
			self.assertTrue(True, "Get One User Day 1 - This should pass. Listing does not exist.")

		db.update_available_quantity(7, 1)
		listing = db.get_one_listing(1)
		self.assertEqual(listing["available_quantity"], 43, "Update Available Quantity Day 1 - Unexpected available quantity after update.")


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

		# g.cursor.execute('''
		# 	insert into public.category (name) values
		# 	('test')
		# ''')
		#
		# db.add_listing({
		# 	'seller_id': 0,
		# 	'title': "test",
		# 	'photo': "",
		# 	'description': "This is a test.",
		# 	'original_quantity': 10,
		# 	'available_quantity': 10,
		# 	'unit_type': "each",
		# 	'price_per_unit': 1.1,
		# 	'total_price': 11.0,
		# 	'category_id': 1,
		# 	'date_harvested': "2018-04-19",
		# 	'is_tradeable': True})
		# resp = self.client.get('/')
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on index.")
		# self.assertTrue(b'Product Feed' in resp.data, "Didn't find title on index.")
		# self.assertTrue(b'test' in resp.data, "Didn't find title of listing on index.")

	def test_listing_detail(self):
		try:
			resp = self.client.get('/listing/1')
			self.assertTrue(False, "Listing Detail Day 0 - This should not be reached. Listing does not exist.")
		except:
			self.assertTrue(True, "Listing Detail Day 0 - This should pass. Listing does not exist.")

		# g.cursor.execute('''
		# 	insert into public.category (name) values
		# 	('test')
		# ''')
		#
		# db.add_listing({
		# 	'seller_id': 0,
		# 	'title': "test",
		# 	'photo': "",
		# 	'description': "This is a test.",
		# 	'original_quantity': 10,
		# 	'available_quantity': 10,
		# 	'unit_type': "each",
		# 	'price_per_unit': 1.1,
		# 	'total_price': 11.0,
		# 	'category_id': 1,
		# 	'date_harvested': "2018-04-19",
		# 	'is_tradeable': True})
		#
		# g.cursor.execute('''
		# 	select * from public.listing limit 1
		# ''')
		#
		# listing = g.cursor.fetchone()
		# self.assertEqual(listing['title'], "test")
		# self.assertEqual(listing['listing_id'], 1)
		#
		# resp = self.client.get('/listing/' + str(listing['listing_id']))
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on listing page.")
		# self.assertTrue(b'test' in resp.data, "Didn't find listing title on listing page.")
		# self.assertTrue(b'1.10' in resp.data, "Didn't find price per unit on listing page.")

	def test_search(self):
		resp = self.client.get('/search')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 0 - Missing site title for no search.")
		self.assertTrue(b'No matches found' in resp.data, "Search Day 0 - Found matches for no search.")

		resp = self.client.get('/search?search=thing')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Search Day 0 - Missing site title on bad search.")
		self.assertTrue(b'No matches found' in resp.data, "Search Day 0 - Found matches for bad search.")

		# resp = self.client.get('/search?search=tes&filter=3')
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on search page.")
		# self.assertTrue(b'No matches found' in resp.data, "Found matches for listing while searching for users.")
		#
		# g.cursor.execute('''
		# 	insert into public.category (name) values
		# 	('test')
		# ''')
		#
		# db.add_listing({
		# 	'seller_id': 0,
		# 	'title': "test",
		# 	'photo': "",
		# 	'description': "This is a test.",
		# 	'original_quantity': 10,
		# 	'available_quantity': 10,
		# 	'unit_type': "each",
		# 	'price_per_unit': 1.1,
		# 	'total_price': 11.0,
		# 	'category_id': 1,
		# 	'date_harvested': "2018-04-19",
		# 	'is_tradeable': True})
		#
		# resp = self.client.get('/search?search=tes')
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on search page.")
		# self.assertTrue(b'test' in resp.data, "Did not find listing when searching for it.")

	def test_buy_listing(self):
		try:
			resp = self.client.get('/listing/buy/1')
			self.assertTrue(False, "Buy Listing Day 0 - This should not be reached. Listing does not exist.")
		except:
			self.assertTrue(True, "Buy Listing Day 0 - This should pass. Listing does not exist.")

		# g.cursor.execute('''
		# 	insert into public.category (name) values
		# 	('test')
		# ''')
		#
		# db.add_listing({
		# 	'seller_id': 0,
		# 	'title': "test",
		# 	'photo': "",
		# 	'description': "This is a test.",
		# 	'original_quantity': 13,
		# 	'available_quantity': 13,
		# 	'unit_type': "each",
		# 	'price_per_unit': 1.1,
		# 	'total_price': 11.0,
		# 	'category_id': 1,
		# 	'date_harvested': "2018-04-19",
		# 	'is_tradeable': True})
		#
		# resp = self.client.get('/listing/buy/1')
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Did not find site title on buy listing page.")
		# self.assertTrue(b'Quantity Available' in resp.data, "Did not find quantity available on buy listing page.")
		# self.assertTrue(b'13' in resp.data, "Did not find expected available quantity on buy listing page.")
		#
		# csrf = getCSRF(resp)
		# resp = self.client.post("/listing/buy/1", data=dict(csrf_token=csrf, quantity=2, submit="Make+Purchase"), follow_redirects=True)
		# self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Did not find site title on listing page.")
		# self.assertTrue(b'Quantity Available' in resp.data, "Did not find quantity available on listing page.")
		# self.assertTrue(b'11' in resp.data, "Did not find expected available quantity on listing page.")
		#
		# resp = self.client.get('/listing/buy/1')
		# csrf = getCSRF(resp)
		# resp = self.client.post("/listing/buy/1", data=dict(csrf_token=csrf, quantity=14, submit="Make+Purchase"), follow_redirects=True)
		# self.assertTrue(b'Make Purchase' in resp.data, "Should still be on buy listing page.")
		# self.assertTrue(b'Please select no more than the quantity that is available.' in resp.data, "Missing flash message.")
		# self.assertTrue(b'Quantity Available' in resp.data, "Did not find quantity available on buy listing page.")
		# self.assertTrue(b'11' in resp.data, "Did not find expected available quantity on buy listing page.")


	def test_new_listing(self):
		# g.cursor.execute('''
		# 	insert into public.category (name) values
		# 	('vegetable')
		# ''')

		resp = self.client.get('/listing/add')
		csrf = getCSRF(resp)
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "New Listing Day 0 - Missing site title.")
		self.assertTrue(b'Title' in resp.data, "New Listing Day 0 - Missing title field.")

		try:
			resp = self.client.post("/listing/buy/1", data=dict(csrf_token=csrf, title="test", photo="", description="This is a test.", original_quantity=10, unit_type="each", price_per_unit=0.97, category_id=1, is_tradeable="y", date_harvested="2018-05-02", submit="Add"), follow_redirects=True)
			self.assertTrue(False, "New Listing Day 0 - This should not be reached. Listing cannot be posted with non-existent category.")
		except:
			self.assertTrue(True, "New Listing Day 0 - This should pass. Listing cannot be posted with non-existent category.")
		# self.assertTrue(b'vegetable' in resp.data, "Did not find expected category on add listing page.")



if __name__ == '__main__':
	unittest.main()
