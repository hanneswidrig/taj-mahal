import db
import pprint as pp

def search(results, q):
	# Run 3 queries
	listings = db.title_like_listings(q)
	categories = db.search_like_category(q)
	users = db.search_like_users(q)
	found_results = (len(listings), len(categories), len(users))
	if found_results[0] > 0:
		results['listings'] = listings	
	if found_results[1] > 0:
		results['categories'] = categories	
	if found_results[2] > 0:
		results['users'] = users	
	# pp.pprint(results)
	print(found_results)
	return results

def filter_choice(listings, filter_id, q):
	if filter_id == 1:
		listings = db.title_like_listings(q)
	elif filter_id == 2:
		categories = db.search_like_category(q)
	elif filter_id == 3:
		users = db.search_like_users(q)
	for listing in listings:
		listing['price_per_unit'] = '${:,.2f}'.format(listing['price_per_unit'])
	return listings
