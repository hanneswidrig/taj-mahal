from flask import g
import psycopg2
import psycopg2.extras
from secrets import database_login_info
import sys

database_config = database_login_info()


def open_db():
    g.connection = psycopg2.connect(database_config)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db():
    g.cursor.close()
    g.connection.close()


def all_listings():
    g.cursor.execute('''SELECT * FROM listing ORDER BY date_created DESC;''')
    return g.cursor.fetchall()


def title_like_listings(search_query):
    search_query = '%' + search_query + '%'
    query = '''
	SELECT * FROM listing WHERE lower(title) LIKE %(search_query)s;
	'''
    g.cursor.execute(query, {'search_query': search_query.lower()})
    return g.cursor.fetchall()


def add_listing(new_product):
    query = '''
		insert into listing(seller_id, title, photo, description, original_quantity, available_quantity, unit_type,
						total_price, price_per_unit, listing_category, is_tradeable, is_active,
						date_created, date_harvested, date_modified)
		values (%(seller_id)s, %(title)s, %(photo)s, %(description)s, %(original_quantity)s,
			%(available_quantity)s, %(unit_type)s, %(total_price)s, %(price_per_unit)s,
			%(listing_category)s, %(is_tradeable)s, true, now(), %(date_harvested)s, now())
		'''
    g.cursor.execute(query, new_product)
    g.connection.commit()
    return g.cursor.rowcount


def get_one_listing(listing_id):
    g.cursor.execute(
        'SELECT * FROM listing WHERE listing_id = %(id)s', {'id': listing_id})
    return g.cursor.fetchone()


def get_one_user(user_id):
		g.cursor.execute('select * FROM "user" WHERE user_id = %(id)s', {'id': user_id})
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
