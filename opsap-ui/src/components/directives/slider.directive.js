/**
 * common directive for slider
 */
const sliderDirective = function(OptionService){
	return {
		restrict: 'AE',
		templateUrl: '/src/components/directives/slider.directive.html',
		replace: true,
		link: function($scope, $element, $attr) {
		  $('#sliderRegular').noUiSlider({
            start: 40,
            connect: "lower",
            range: {
                min: 0,
                max: 100
            }
        });
		}
	}
}

sliderDirective.$inject = ['OptionService'];

module.exports = sliderDirective;