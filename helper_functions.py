import sys
import re

def relative_link(request_path, request_referrer): 
	path = request_path
	referrer = request_referrer
	if path is None:
		return '/'

	if referrer is None:
		referrer = ''

	listing_detail = re.compile('/listing/\d*$').findall(path)
	buy_listing    = re.compile('/listing/buy/\d*$').findall(path)
	search         = re.findall('/search', referrer)
	index          = re.compile('\/[0-9]+').findall(path)

	if listing_detail and not search:
		return '/'
	elif buy_listing:
		return '/listing'+index[0]
	elif search:
		return referrer
	elif index:
		return '/'