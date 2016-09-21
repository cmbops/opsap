/**
 * navbar
 */
const $inject = ['$scope', '$window', 'VMService'];
const NavController = function($scope, $window, VMService) {
	this.title = 'index';
	this.asyncGetChartsData = asyncGetChartsData;

	function asyncGetChartsData() {
		 return [34,54,70];
	}
}

NavController.$inject = $inject;
module.exports = NavController

