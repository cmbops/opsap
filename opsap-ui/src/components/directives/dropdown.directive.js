/**
 * common directive for tablerender
 */

const dropdownDirective = function(OptionService){
	return {
		restrict: 'AE',
		templateUrl: '/src/components/directives/dropdown.directive.html',
		replace: true,
		link: function($scope, $element, $attr) {
			$element.find('a').bind('click', function(){
				console.log('test');
				$element.find('button').text($(this).text()).append('&nbsp;<span class="caret"></span>');
				
			});
		}
	}
}

dropdownDirective.$inject = ['OptionService'];

module.exports = dropdownDirective;