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
    g.cursor.execute('''SELECT * FROM listing WHERE available_quantity > 0 ORDER BY date_created DESC;''')
    return g.cursor.fetchall()


def title_like_listings(search_query):
    search_query = '%' + search_query + '%'
    query = '''
		SELECT * FROM listing WHERE lower(title) LIKE %(search_query)s;
		'''
    g.cursor.execute(query, {'search_query': search_query.lower()})
    return g.cursor.fetchall()


def search_like_category(search_query):
    search_query = '%' + search_query + '%'
    query = '''
		SELECT * FROM listing inner join category on listing.category_id = category.category_id
		WHERE name LIKE %(search_query)s;
		'''
    g.cursor.execute(query, {'search_query': search_query.lower()})
    return g.cursor.fetchall()


def search_like_users(search_query):
    search_query = '%' + search_query + '%'
    query = '''
		select * from "user" 
		where lower(email) LIKE  %(search_query)s 
		or lower(first_name) LIKE  %(search_query)s 
		or lower(last_name) LIKE  %(search_query)s;
		'''
    g.cursor.execute(query, {'search_query': search_query.lower()})
    return g.cursor.fetchall()


def add_listing(new_product):
    query = '''
		insert into listing(seller_id, title, photo, description, original_quantity, available_quantity, unit_type,
						total_price, price_per_unit, category_id, is_tradeable, is_active,
						date_created, date_harvested, date_modified)
		values (%(seller_id)s, %(title)s, %(photo)s, %(description)s, %(original_quantity)s,
			%(available_quantity)s, %(unit_type)s, %(total_price)s, %(price_per_unit)s,
			%(category_id)s, %(is_tradeable)s, true, now(), %(date_harvested)s, now());
		'''
    g.cursor.execute(query, new_product)
    g.connection.commit()
    return g.cursor.rowcount


def get_one_listing(listing_id):
    g.cursor.execute('SELECT * FROM listing WHERE listing_id = %(id)s;', {'id': listing_id})
    return g.cursor.fetchone()


def get_one_user(user_id):
		g.cursor.execute('SELECT * FROM "user" WHERE user_id = %(id)s;', {'id': user_id})
		return g.cursor.fetchone()

def find_user(email):
	g.cursor.execute('SELECT * FROM "user" WHERE email = %(email)s;', {'email': email})
	return g.cursor.fetchone()

def get_one_login(email):
	g.cursor.execute('SELECT * FROM "user" WHERE email = %(email)s;', {'email': email})
	return g.cursor.fetchone()



def get_user_listings(user_id):
		g.cursor.execute('SELECT * FROM listing where seller_id = %(id)s;', {'id': user_id})
		return g.cursor.fetchall()


def update_available_quantity(bought_amount, listing_id):
    query = '''
		UPDATE listing
		SET available_quantity = available_quantity - %(bought_amount)s
		WHERE listing_id = %(id)s;
		'''
    g.cursor.execute(query, {'id': listing_id, 'bought_amount': bought_amount})
    g.connection.commit()
    return g.cursor.rowcount

  
def get_user_address(user_id):
		query = '''
		SELECT street, city, state.name, abbrev, zipcode FROM ("user"
  	INNER JOIN address on "user".address_id = address.address_id
  	INNER JOIN state on address.state_id = state.state_id)
		WHERE "user".user_id = %(id)s;
		'''
		g.cursor.execute(query, {'id': user_id})
		return g.cursor.fetchone()


def get_user_address_via_listing(listing_id):
		query = '''
		SELECT street, city, state.name, abbrev, zipcode FROM (listing
  	INNER JOIN "user" on listing.seller_id = "user".user_id
  	INNER JOIN address on "user".address_id = address.address_id
  	INNER JOIN state on address.state_id = state.state_id) 
		WHERE listing.listing_id = %(id)s;
		'''
		g.cursor.execute(query, {'id': listing_id})
		return g.cursor.fetchone()


def get_listing_details_for_confirmation_page(listing_id):
		query = '''
		SELECT listing.title, listing.photo, listing.unit_type,
		"user".first_name, "user".last_name FROM (listing
		INNER JOIN "user" on listing.seller_id = "user".user_id)
		WHERE listing.listing_id = %(listing_id)s;
		'''
		g.cursor.execute(query, {'listing_id': listing_id})
		return g.cursor.fetchone()


def add_new_order(listing_id, qty, total_cost, buyer_id):
		query = '''
		INSERT into orders(listing_id, quantity, total_cost, buyer_id, time_placed)
		values(%(listing_id)s, %(qty)s, %(total_cost)s, %(buyer_id)s, now());
		'''
		g.cursor.execute(query, {
			'listing_id': listing_id, 
			'qty': qty, 
			'total_cost': total_cost,
			'buyer_id': buyer_id})
		g.connection.commit()
		return g.cursor.rowcount


# def find_user(userEmail):
#     """Look up a single user."""
#     # query = """
#     # SELECT m.email, m.first_name, m.last_name, p.file_path
#     # FROM user AS m
#     #    LEFT OUTER JOIN photo AS p ON m.email = p.user_email
#     # WHERE email = %(emailParam)s
#     # """
#     query = """
#         SELECT email, first_name, last_name
#         FROM user
#         WHERE email = %(emailParam)s
#         """
#     g.cursor.execute(query, {'emailParam': userEmail})
#     return g.cursor.fetchone()


def create_user(email, first_name, last_name, photo, password, bio):
    """Create a new user."""
    query = '''
INSERT INTO public.user(address_id, email, first_name, last_name, profile_pic, password, bio)
VALUES (1, %(email)s, %(first)s, %(last)s, %(photo)s, %(pass)s, %(bio)s)
    '''
    g.cursor.execute(query, {'email': email, 'first': first_name, 'last': last_name, 'photo': photo, 'pass': password, 'bio': bio})
    g.connection.commit()
    return g.cursor.rowcount
