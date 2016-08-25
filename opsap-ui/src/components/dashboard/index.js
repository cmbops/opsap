module.exports = angular.module('opsap.dashboard', [])
                   .controller('NavController', require('./NavController'))
                   .directive('menuTab', require('../directives/menu.directive'))