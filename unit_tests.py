import unittest

from flask import g

import db
from app import app


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


class DatabaseTestCase(FlaskTestCase):
	"""Setup Cursor for Testing"""
	@staticmethod
	def execute_sql(resource_name):
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		super(DatabaseTestCase, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')

	def tearDown(self):
		db.close_db()
		super(DatabaseTestCase, self).tearDown()
	"""------------------------"""

	def test_all_listings(self):
		listings = db.all_listings()
		self.assertEqual(len(listings), 0)

		self.execute_sql("db\seed_tables.sql")

		listings = db.all_listings()
		self.assertEqual(len(listings), 5)

	def test_title_like_listings(self):
		g.cursor.execute('''
			insert into public.category (name) values
			('test')
		''')

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
		self.assertEqual(len(listings), 1)

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
		self.assertEqual(len(listings), 2)

	def test_add_listing(self):
		g.cursor.execute('''
			insert into public.category (name) values
			('test')
		''')

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
		self.assertEqual(row_count, 1)

		g.cursor.execute(
			"SELECT * FROM listing WHERE title='addtest'")
		listing = g.cursor.fetchone()
		self.assertIsNotNone(listing)

		listing = db.get_one_listing(listing['listing_id'])
		self.assertIsNotNone(listing)

	def test_get_one_user(self):
		g.cursor.execute('''
insert into public.user (address_id, username, password, first_name, last_name, profile_pic, bio) values
(0, 'test', 'test', 'tester', 'tester', '', 'This is a test.')
		''')

		g.cursor.execute('''
select * from public.user where username = 'test'
		''')

		user = g.cursor.fetchone()
		user = db.get_one_user(user["user_id"])

		self.assertEqual(user["username"], "test")
		self.assertEqual(user["first_name"], "tester")

	def test_update_available_quantity(self):
		g.cursor.execute('''
			insert into public.category (name) values
			('test')
		''')

		db.add_listing({
			'seller_id': 0,
			'title': "test",
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

		g.cursor.execute('''
select * from public.listing where title='test'
		''')
		listing = g.cursor.fetchone()

		db.update_available_quantity(4, listing['listing_id'])

		g.cursor.execute('''
select * from public.listing where title='test'
		''')
		listing = g.cursor.fetchone()

		self.assertEqual(listing['available_quantity'], 6)


class ApplicationTestCase(FlaskTestCase):
	"""Setup Cursor for Testing"""
	@staticmethod
	def execute_sql(resource_name):
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		super(ApplicationTestCase, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')

	def tearDown(self):
		db.close_db()
		super(ApplicationTestCase, self).tearDown()
	"""------------------------"""

	def test_index(self):
		g.cursor.execute('''
			insert into public.category (name) values
			('test')
		''')

		resp = self.client.get('/')
		self.assertTrue(b'Product Feed' in resp.data, "Didn't find title on index.")
		self.assertTrue(b'No search results found' in resp.data, "Didn't find title of listing on index.")

		db.add_listing({
			'seller_id': 0,
			'title': "test",
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
		resp = self.client.get('/')
		self.assertTrue(b'Product Feed' in resp.data, "Didn't find title on index.")
		self.assertTrue(b'test' in resp.data, "Didn't find title of listing on index.")

	#def test_member_page(self):
	#	"""Verify the member page."""
	#	resp = self.client.get(url_for('all_members'))
	#	self.assertTrue(b'Comments' in resp.data)


if __name__ == '__main__':
	unittest.main()
