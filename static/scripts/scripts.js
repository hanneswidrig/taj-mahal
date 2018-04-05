$(document).ready(function() {
	if (window.location.pathname == "/" || window.location.pathname == "") {
		$('#index').addClass("nav-item-active");
	}
	else if (window.location.pathname == "/listing/add") {
		$('#add').addClass("nav-item-active");
	}
	else if (window.location.pathname == "/user") {
		$('#account').addClass("nav-item-active");
	}
});