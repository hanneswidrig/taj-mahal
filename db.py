from flask import g
import psycopg2
import psycopg2.extras
from secrets import database_login_info
import sys

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

def title_like_listings(search_query):
	percent = '%'
	query = '''SELECT * FROM listing WHERE lower(title) LIKE concat(%(percent)s, lower(%(search_query)s), %(percent)s);'''
	g.cursor.execute(query, {'search_query': search_query, 'percent': percent})
	return g.cursor.fetchall()


def add_listing(id, title, photo, description, original_quantity, unit_type, price_per_unit, listing_category, listing_quality, is_tradeable, expiration_date):
	query = '''
		insert into listing(seller_id, title, photo, description, original_quantity, available_quantity, unit_type,
							total_price, price_per_unit, listing_category, listing_quality, is_tradeable, is_active,
							date_created, expiration_date, date_modified)
		values (%(seller_id)s, %(title)s, %(photo)s, %(description)s, %(original_quantity)s,
				%(available_quantity)s, %(unit_type)s, %(total_price)s, %(price_per_unit)s,
				%(listing_category)s, %(listing_quality)s, %(is_tradeable)s, true, now(), %(expiration_date)s, now())
	'''

	g.cursor.execute(query, {'seller_id': id, 'title': title, 'photo': photo, 'description': description,
	                         'original_quantity': original_quantity, 'available_quantity': original_quantity,
	                         'unit_type': unit_type, 'total_price': (price_per_unit * original_quantity),
	                         'price_per_unit': price_per_unit, 'listing_category': listing_category,
	                         'listing_quality': listing_quality, 'is_tradeable': is_tradeable,
	                         'expiration_date': expiration_date})
	g.connection.commit()
	return g.cursor.rowcount


def get_one_listing(listing_id):
	g.cursor.execute('SELECT * FROM listing WHERE listing_id = %(id)s', {'id': listing_id})
	return g.cursor.fetchone()


def update_available_quantity(bought_amount, id):
	query = '''
	UPDATE listing
	SET available_quantity = available_quantity - %(bought_amount)s
	WHERE listing_id = %(id)s
	'''
	g.cursor.execute(query, {'id': id, 'bought_amount': bought_amount})
	g.connection.commit()
	return g.cursor.rowcount 

