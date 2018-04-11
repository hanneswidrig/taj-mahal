$(document).ready(function() {
	activePageMobile();
	activePageDesktop();
	expandFilters();

	function activePageMobile() {
		if (window.location.pathname == '/' || window.location.pathname == '') {
			$('#index').addClass('nav-item-active');
		} else if (window.location.pathname == '/listing/add') {
			$('#add').addClass('nav-item-active');
		} else if (window.location.pathname == '/search') {
			$('#search').addClass('nav-item-active');
		} else if (window.location.pathname == '/user') {
			$('#account').addClass('nav-item-active');
		}
	}
	function activePageDesktop() {
		if (window.location.pathname == '/' || window.location.pathname == '') {
			$('#index-d').addClass('dsktp-item-active');
		} else if (window.location.pathname == '/listing/add') {
			$('#add-d').addClass('dsktp-item-active');
		} else if (window.location.pathname == '/user') {
			$('#account-d').addClass('dsktp-item-active');
		}
	}
	function expandFilters() {
		$('.filter-toggle').on('click', function(e) {
			e.preventDefault();
			console.log('You clicked Filter');
			// $('.app-bar').toggleClass('expanded-filter');
		});
	}
});
