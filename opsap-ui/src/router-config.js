/**
 * router config for opsap
 */
const COMMON_URL = '/src/components';
const $inject = ['$stateProvider', '$urlRouterProvider'];
const routerConfig = function($stateProvider,  $urlRouterProvider) {

	$urlRouterProvider.when('','/index');
	$urlRouterProvider.otherwise('/index');
    

	$stateProvider
	  .state('login', {
	  	  url: '/login',
	  	  template: require('./components/login/login.html'),
	  	  controller: 'LoginController as login',
	  }) 
	  .state('index', {
	  	  url: '/index',
	  	  template: require('./components/dashboard/nav.html'),
	  	  data: { requireLogin: true},
	  	  controller: 'NavController as nav'
	  })
	  .state('index.user', {
	  	  url: '/user/:operation',
	  	  templateUrl: function($stateParams) {
	  	  	return COMMON_URL + '/user/user_' + $stateParams.operation + '.html'
	  	  },
	  	  controller:'UserController as user'
	  })
	  .state('index.usergroup', {
	  	url: '/usergroup/:operation',
	  	templateUrl: function($stateParams) {
	  		return COMMON_URL +
	  		 '/user/group_' + $stateParams.operation + '.html'
	  	},
	  	controller: 'UserGroupController as usergroup'
	  })
	  .state('index.vmmanager', {
	  	url: '/vmmanager/:operation',
	  	templateUrl: function($stateParams) {
	  		return COMMON_URL + '/vmmanager/vmresource_' + $stateParams.operation + '.html'
	  	}
	  })
	  .state('index.datamanager', {
	  	url: '/datamanager',
	  	template: require('./components/datamanager/data_list.html')
	  })
}

routerConfig.$inject = $inject;
module.exports = routerConfig;