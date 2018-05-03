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

	def test_search_like_category(self):
		listings = db.search_like_category("veg")
		self.assertEqual(len(listings), 0)

		g.cursor.execute('''
			insert into public.category (name) values
			('vegetable')
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

		listings = db.search_like_category("veg")
		self.assertEqual(len(listings), 1)

		g.cursor.execute('''
			insert into public.category (name) values
			('fruit')
		''')

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

		db.add_listing({
			'seller_id': 0,
			'title': "addtest3",
			'photo': "",
			'description': "This is a test.",
			'original_quantity': 10,
			'available_quantity': 10,
			'unit_type': "each",
			'price_per_unit': 1.1,
			'total_price': 11.0,
			'category_id': 2,
			'date_harvested': "2018-04-19",
			'is_tradeable': True})

		listings = db.search_like_category("veg")
		self.assertEqual(len(listings), 2)

	def test_search_like_users(self):
		users = db.search_like_users("ha")
		self.assertEqual(len(users), 0)
		
		self.execute_sql("db\seed_tables.sql")
		
		users = db.search_like_users("hann")
		self.assertEqual(len(users), 1)
		users = db.search_like_users("ha")
		self.assertEqual(len(users), 2)

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
		resp = self.client.get('/')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on index.")
		self.assertTrue(b'Product Feed' in resp.data, "Didn't find title on index.")
		self.assertTrue(b'No search results found' in resp.data, "Didn't find default response for no listings.")

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
		resp = self.client.get('/')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on index.")
		self.assertTrue(b'Product Feed' in resp.data, "Didn't find title on index.")
		self.assertTrue(b'test' in resp.data, "Didn't find title of listing on index.")

	def test_listing_detail(self):
		try:
			resp = self.client.get('/listing/1')
			self.assertTrue(b'Gardener\'s Exchange' in resp.data, "This should fail for non-existent listing.")
		except:
			self.assertTrue(True, "This should pass.")

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
			select * from public.listing limit 1
		''')

		listing = g.cursor.fetchone()
		self.assertEqual(listing['title'], "test")
		self.assertEqual(listing['listing_id'], 1)

		resp = self.client.get('/listing/' + str(listing['listing_id']))
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on listing page.")
		self.assertTrue(b'test' in resp.data, "Didn't find listing title on listing page.")
		self.assertTrue(b'1.10' in resp.data, "Didn't find price per unit on listing page.")

	def test_search(self):
		resp = self.client.get('/search')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on search page.")
		self.assertTrue(b'No matches found' in resp.data, "Found matches for no search.")

		resp = self.client.get('/search?search=thing')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on search page.")
		self.assertTrue(b'No matches found' in resp.data, "Found matches for bad search.")

		resp = self.client.get('/search?search=tes&filter=3')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on search page.")
		self.assertTrue(b'No matches found' in resp.data, "Found matches for listing while searching for users.")

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

		resp = self.client.get('/search?search=tes')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Didn't find site title on search page.")
		self.assertTrue(b'test' in resp.data, "Did not find listing when searching for it.")

	def test_buy_listing(self):
		try:
			resp = self.client.get('/listing/buy/1')
			self.assertTrue(b'Gardener\'s Exchange' in resp.data, "This should fail for non-existent listing.")
		except:
			self.assertTrue(True, "This should pass.")

		g.cursor.execute('''
			insert into public.category (name) values
			('test')
		''')

		db.add_listing({
			'seller_id': 0,
			'title': "test",
			'photo': "",
			'description': "This is a test.",
			'original_quantity': 13,
			'available_quantity': 13,
			'unit_type': "each",
			'price_per_unit': 1.1,
			'total_price': 11.0,
			'category_id': 1,
			'date_harvested': "2018-04-19",
			'is_tradeable': True})

		resp = self.client.get('/listing/buy/1')
		self.assertTrue(b'Gardener\'s Exchange' in resp.data, "Did not find site title on buy listing page.")
		self.assertTrue(b'Quantity Available' in resp.data, "Did not find quantity available on buy listing page.")
		self.assertTrue(b'13' in resp.data, "Did not find expected available quantity on buy listing page.")

		# app.post("/listing/buy/1", data=dict(quantity=2))

	def test_new_listing(self):
		self.assertTrue(True, "")


if __name__ == '__main__':
	unittest.main()
