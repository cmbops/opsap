
require('../services/vm.service')
module.exports = angular.module('opsap.dashboard', ['vmService'])
                   .controller('NavController', require('./NavController'))
                   .directive('menuTab', require('../directives/menu.directive'))
                   .directive('echartsBar', require('../directives/echarts.directive'))