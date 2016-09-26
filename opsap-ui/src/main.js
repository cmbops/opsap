/**
 * 主页面入口
 */

//css文件依赖
require('./assets/css/bootstrap.min.css')
require('./assets/css/material-kit.css')
require('./assets/css/style.css')
require('./assets/css/loading.css')
require('./assets/css/rzslider.min.css')
require('./assets/css/font-awesome.min.css')
require('./assets/css/animate.css')

//js文件依赖

//angular依赖
require('angular-ui-router');
require('angular-ui-bootstrap');
require('./baseService');

var opsap = angular.module('opsap', [
	'ui.router',
	'ui.bootstrap',
	'baseService',
	'rzModule',
	require('./components/login').name,
	require('./components/dashboard').name,
	require('./components/user').name,
	require('./components/vmmanager').name,
	require('./components/datamanager').name,
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
			console.log('%o || %o || %o', toState, fromState, $window.sessionStorage);
			if(toState != null && toState.data != null && toState.data.requireLogin && !AuthenticationService.isLogged && !$window.sessionStorage.token){
				event.preventDefault();
				$state.go('login');
			}
			console.log(AuthenticationService.isLogged);
		})
}])
module.exports = opsap;
/*require('./src/css/style.css');*/