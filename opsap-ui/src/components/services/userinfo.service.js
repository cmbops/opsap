/**
 * userinfo service
 */
require('../../baseService');

var userinfoservice = angular.module('userinfoService', ['baseService']);

userinfoservice.factory('UserManagementService', ['$rootScope', 'BaseService', function($rootScope, BaseService){
	var usermanagement = {
		getUsers: getUsers,
		getUserGroups: getUserGroups
	}

	return usermanagement;

	function getUsers() {
		return BaseService.GET('../src/components/data/user.json');
	}

	function getUserGroups() {
		return BaseService.GET('../src/components/data/usergroup.json');
	}

}])

module.exports = userinfoservice;