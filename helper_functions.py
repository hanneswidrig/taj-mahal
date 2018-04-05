import sys
import re

def relative_link(request_path): 
	rel_link = request_path

	if rel_link is None:
		return '/'

	listing_detail = re.compile('/listing/\d*$').findall(rel_link)
	buy_listing    = re.compile('/listing/buy/\d*$').findall(rel_link)
	index          = re.compile('\/[0-9]+').findall(rel_link)

	# print(listing_detail)
	# print(buy_listing)
	# print(index)
	# print('\n'+rel_link+'\n')

	if listing_detail:
		return '/'
	elif buy_listing:
		return '/listing'+index[0]
	elif index:
		return '/'