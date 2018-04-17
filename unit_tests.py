import tempfile
import unittest
import os

from flask import g, url_for

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
	@staticmethod
	def execute_sql(resource_name):
		"""Helper function to run a SQL script on the test database."""
		with app.open_resource(resource_name, mode='r') as f:
			g.cursor.execute(f.read())
		g.connection.commit()

	def setUp(self):
		"""Open the database connection and create all the tables."""
		super(DatabaseTestCase, self).setUp()
		db.open_db()
		self.execute_sql('db\create_tables.sql')

	def tearDown(self):
		"""Clear all tables in the database and close the connection."""
		db.close_db()
		super(DatabaseTestCase, self).tearDown()

	def test_add_listing(self):
		self.assertEqual(1, 1)

	def test_get_one_listing(self):
		self.fail()


if __name__ == '__main__':
	unittest.main()
