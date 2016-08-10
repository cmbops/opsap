require('angular-ui-router');
require('./baseService');

var angular = require('angular');

var opsap = angular.module('opsap', [
	'ui.router',
	'baseService',
	require('./components/login').name,
	require('./components/dashboard').name,
	require('./components/user').name
	])

//控制器
/*opsap.controller('LoginController', require('./components/login/loginController'));
opsap.controller('NavController', require('./components/dashboard/NavController'))
*/


//模块opsap基本配置
opsap.config(['$httpProvider', function($httpProvider) {
	//每个$http请求都认证authorization
	$httpProvider.interceptors.push('TokenInterceptor');
}])

//配置路由
opsap.config(require('./router-config'))

//每个页面刷新检测是否登录
opsap.run(['$rootScope', '$state', '$window','AuthenticationService', function($rootScope, $state, $window, AuthenticationService){
	$rootScope.$on('$stateChangeStart', 
		function(event, toState, toParams, fromState, fromParams){
			if(toState != null && toParams.data != null && toParams.data.requireLogin && !AuthenticationService.isLogged && !$window.sessonStorage.token){
				event.preventDefault();
				$state.go('login');
			}
			console.log(AuthenticationService.isLogged);
		})
}])
module.exports = opsap;
/*require('./src/css/style.css');*/