/**
 * router config for opsap
 * 路由控制
 */
const COMMON_URL = '/src/components';
const usertemplates = {list:require('./components/user/user_list.html'), add:require('./components/user/user_add.html')};
const usergrouptemplates = {list:require('./components/user/group_list.html'), add:require('./components/user/group_add.html')};
const vmtemplates = {apply:require('./components/vmmanager/vmresource_apply.html'), 
                     list:require('./components/vmmanager/vmresource_list.html'),
                     manage: require('./components/vmmanager/vmresource_manage.html'),
                     verify: require('./components/vmmanager/vmresource_verify.html')
                 }
const dmtemplates = {list: require('./components/datamanager/data_list.html'),
                     check: require('./components/datamanager/data_check.html')    
				}
const Page404 = '<h1>404 page not found</h1>'
/*const userlistTmp = require('./components/user/user_list.html');
const useraddTmp = require('./components/user/user_add.html');*/
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
	  .state('index.dashboard', {
	  	  url: '/dash',
	  	  template: require('./components/dashboard/charts.html'),
	  	  controller: 'NavController as nav'
	  })
	  .state('index.user', {
	  	  url: '/user/:operation',
	  	  templateProvider: ['$timeout', '$stateParams',function($timeout, $stateParams) {
	  	  	return $timeout(function() {
	  	  		return getTmp(usertemplates, $stateParams.operation);
	  	  	}, 100)
	  	  }],
	  	  controller:'UserController as user'
	  })
	  .state('index.usergroup', {
	  	url: '/usergroup/:operation',
	  	templateProvider: ['$timeout', '$stateParams',function($timeout, $stateParams) {
	  	  	return $timeout(function() {
	  	  		return getTmp(usergrouptemplates, $stateParams.operation);
	  	  	}, 100)
	  	  }],
	  	controller: 'UserGroupController as usergroup'
	  })
	  .state('index.vmmanager', {
	  	url: '/vmmanager/:operation',
	  	templateProvider: ['$timeout', '$stateParams',function($timeout, $stateParams) {
	  	  	return $timeout(function() {
	  	  		return getTmp(vmtemplates, $stateParams.operation);
	  	  	}, 100)
	  	  }],
	  })
	  .state('index.datamanager', {
	  	url: '/datamanager:operation',
		templateProvider: ['$timeout', '$stateParams',function($timeout, $stateParams) {
	  	  	return $timeout(function() {
	  	  		return getTmp(dmtemplates, $stateParams.operation);
	  	  	}, 100)
	  	  }]
	  })

	  function getTmp(templates, operation) {
	  	return templates[operation] ? templates[operation] : Page404;
	  }
}

routerConfig.$inject = $inject;
module.exports = routerConfig;