/**
 * common directive for tablerender
 */

const tablerenderDirective = function(){
	return {
		restrict: 'AE',
		template: require('./tablerender.directive.html'),
		scope: {
			titles: '=',
			contents: '=',
			operate: '@'
		},
		transclude: true
	}
}

tablerenderDirective.$inject = [];

module.exports = tablerenderDirective;