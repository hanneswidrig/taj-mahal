from flask import g
import psycopg2
import psycopg2.extras
from secrets import database_login_info

database_config = database_login_info()

def open_db():
	g.connection = psycopg2.connect(database_config)
	g.cursor     = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

def close_db():
	g.cursor.close()
	g.connection.close()

def all_listings():
	g.cursor.execute('''SELECT * FROM listing ORDER BY date_created DESC;''')
	return g.cursor.fetchall()

def get_one_listing(listing_id):
	g.cursor.execute('SELECT * FROM listing WHERE listing_id = %(id)s', {'id': listing_id})
	return g.cursor.fetchone()