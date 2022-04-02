$(document).ready(function(){
	// Mobile navigation switcher
	$('.toggle-nav').on('click', function(){
		$(this).toggleClass('active');
		$('.wrapper').toggleClass('slide');
	});

	$(window).resize(function() {
		if ($(window).width() > 463) {
			$('.toggle-nav').removeClass('active');
			$('.wrapper').removeClass('slide');
		}
	});
	
	// Language selection
	function formatLanguage(language) {

		if (!language.id) { return language.text; }
		var $language = $(
			'<span class="flag-icon flag-icon-'+ language.id.toLowerCase() +'"></span>' +
			'<span class="flag-text">'+ language.text +"</span>"
		);
		return $language;
	};
	 $('#id_language').select2({
	 	templateResult: formatLanguage,
	 	minimumResultsForSearch: -1
	 });

	// Slide down Bill Type update field	
	$(".abt-edit-type").click(function() {
		$id = $(this).attr('id');
		$('#abt-list-update-' + $id).slideDown("fast");
	});

	$( ".abt-input-clear" ).click(function() {
		$id = $(this).attr('id');
		$('#abt-list-update-' + $id).slideUp("fast");
	});

	// Get Tab parameters in Settings page
	$tab = $.url("query").split("=")[1];
	if ($('.tab-checkbox').hasClass($tab)) {
		$('.tab-checkbox' + '.' + $tab).attr('checked', 'checked');
	}

	// Clean URL
	var uri = window.location.toString();
	$('.tab-checkbox').on('click', function(){
		if (uri.indexOf("?") > 0) {
		    var clean_uri = uri.substring(0, uri.indexOf("?"));
		    window.history.replaceState({}, document.title, clean_uri);
		}
	});
	
});