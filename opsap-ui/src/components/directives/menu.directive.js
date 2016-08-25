/**
 * common directive for menubar
 */

const menuDirective = function(){
	return {
		restrict: 'AE',
		template: '<div class="navbar-header">' 
		+ '<a class="navbar-minimalize minimalize-styl-2 btn btn-primary" >'
		+ '<i class="fa fa-bars"></i> </a></div>',
		replace: true,
		link: function($scope, $element, $attr) {
	        

			$('.navbar-minimalize').on('click', function() {
			    $("body").toggleClass("mini-navbar");
			    SmoothlyMenu();
			})

			function SmoothlyMenu() {
			    if (!$('body').hasClass('mini-navbar') || $('body').hasClass('body-small')) {
			        // Hide menu in order to smoothly turn on when maximize menu
			        $('#side-menu').hide();
			        // For smoothly turn on menu
			        setTimeout(
			            function() {
			                $('#side-menu').fadeIn(500);
			            }, 100);
			    } else if ($('body').hasClass('fixed-sidebar')) {
			        $('#side-menu').hide();
			        setTimeout(
			            function() {
			                $('#side-menu').fadeIn(500);
			            }, 300);
			    } else {
			        // Remove all inline style from jquery fadeIn function to reset menu state
			        $('#side-menu').removeAttr('style');
			    }
			}



		}
	}
}

menuDirective.$inject = [];

module.exports = menuDirective;