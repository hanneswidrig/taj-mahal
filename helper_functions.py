def relative_link(request_referrer):
	rel_link = request_referrer
	if rel_link is None:
		rel_link = '/'
	return rel_link