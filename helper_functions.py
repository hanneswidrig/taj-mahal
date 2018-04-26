import sys
import re

def relative_link(request_path, request_referrer): 
	path = request_path
	referrer = request_referrer
	if path is None:
		return '/'

	if referrer is None:
		referrer = ''

	listing_detail   = re.compile(r'/listing/\d*$').findall(path)
	listing_purchase = re.compile(r'/listing/buy/\d*$').findall(path)
	search           = re.findall('/search', referrer)
	index            = re.compile(r'\/[0-9]+').findall(path)

	if listing_detail and not search:
		return '/'
	elif listing_purchase:
		return '/listing'+index[0]
	elif search:
		return referrer
	elif index:
		return '/'