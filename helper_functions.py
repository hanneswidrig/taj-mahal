import sys
import re

def relative_link(request_path, request_referrer): 
	if request_path is None:
		return '/'

	listing_detail = re.compile('/listing/\d*$').findall(request_path)
	buy_listing    = re.compile('/listing/buy/\d*$').findall(request_path)
	search         = re.findall('/search', request_referrer)
	index          = re.compile('\/[0-9]+').findall(request_path)

	if listing_detail and not search:
		return '/'
	elif buy_listing:
		return '/listing'+index[0]
	elif search:
		return request_referrer
	elif index:
		return '/'