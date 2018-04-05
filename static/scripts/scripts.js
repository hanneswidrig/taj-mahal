$(document).ready(function() {
	if (window.location.href == "http://localhost:5000/") {
		$('#index').addClass("nav-item-active");
	}
	else if (window.location.href == "http://localhost:5000/listing/add") {
		$('#add').addClass("nav-item-active");
	}
	else if (window.location.href == "http://localhost:5000/user") {
		$('#user').addClass("nav-item-active");
	}
});