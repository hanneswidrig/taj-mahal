$(document).ready(function() {
	activePageMobile();
	activePageDesktop();
	chooseFilter();
	fileUpload();

	function activePageMobile() {
		if (window.location.pathname == '/' || window.location.pathname == '') {
			$('#index').addClass('nav-item-active');
		} else if (window.location.pathname == '/listing/add') {
			$('#add').addClass('nav-item-active');
		} else if (window.location.pathname == '/search') {
			$('#search').addClass('nav-item-active');
		} else if (window.location.pathname == '/account') {
			$('#account').addClass('nav-item-active');
		}
	}
	function activePageDesktop() {
		if (window.location.pathname == '/' || window.location.pathname == '') {
			$('#index-d').addClass('dsktp-item-active');
		} else if (window.location.pathname == '/listing/add') {
			$('#add-d').addClass('dsktp-item-active');
		} else if (window.location.pathname == '/account') {
			$('#account-d').addClass('dsktp-item-active');
		}
	}
	function fileUpload() {
		$('#cFile').change(function() {
			var i = $(this).prev('.custom-file-label').clone();
			var file = $('#cFile')[0].files[0].name;
			$(this).prev('.custom-file-label').text(file);
		});
	}
	function createFilterURL(filterID) {
		var url = new URL(window.location.href);
		var getFilter = new XMLHttpRequest();
		if (url.searchParams.get('filter') != filterID) {
			url.searchParams.set('filter', filterID);
			getFilter.open('GET', url.href, true);
			getFilter.send();
			window.location.replace(url.href);
		}
		if(location.search.indexOf('filter=') == -1) {
			var filter_query = '&filter=' + filterID;
			if(location.search.indexOf('search=') == -1) {
				filter_query = '?filter=' + filterID;
			}
			var final_url = window.location.href + filter_query;
			getFilter.open('GET', final_url, true);
			getFilter.send();
			window.location.replace(final_url);
		}
	}
	function chooseFilter() {
		$('#f1').on('click', function(e) {
			e.preventDefault();
			createFilterURL('1');
		})
		$('#f2').on('click', function(e) {
			e.preventDefault();
			createFilterURL('2');
			
		})
		$('#f3').on('click', function(e) {
			e.preventDefault();
			createFilterURL('3');
		})
	}
	
});
