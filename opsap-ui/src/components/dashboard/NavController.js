/**
 * navbar
 */
const $inject = ['$scope'];
const NavController = function($scope, $window) {
	this.title = 'index';
}

NavController.$inject = $inject;
module.exports = NavController

