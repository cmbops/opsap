/**
 * common directive for tablerender
 */

const tablerenderDirective = function(){
	return {
		restrict: 'AE',
		templateUrl: 'tablerender.directive.html'
	}
}

tablerenderDirective.$inject = [];

module.exports = tablerenderDirective;