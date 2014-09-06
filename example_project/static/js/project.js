/* Project specific Javascript goes here. */

$(document).ready(function() {
	// Highlight in the navigation bar the active menu item.
	var path = window.location['pathname'];
	if (path == '/') {
		$('ul.navbar-nav li.home').addClass('active');
	} else if (path.substring(0, 6) == '/news/') {
		$('ul.navbar-nav li.news').addClass('active');
	}
})