/**
 * userinfo service
 */
require('../../baseService');

var userinfoservice = angular.module('userinfoService', ['baseService']);

userinfoservice.factory('UserManagementService', ['$rootScope', 'BaseService', function($rootScope, BaseService){
	var usermanagement = {
		getUsers: getUsers,
		getUserList: getUserList,
		getUserGroups: getUserGroups,
		addUser: addUser,
		addUserGroup: addUserGroup
	}

	return usermanagement;

	function getUsers() {
		return BaseService.GET('../src/components/data/user.json');
	}

	function getUserGroups() {
		return BaseService.GET('../src/components/data/usergroup.json');
	}

	function addUser(params) {
		return BaseService.POST(url, params);
	}

    //返回用户列表
	function getUserList() {
		return BaseService.GET('../src/components/data/user.json').then(selectUsername);
	}

	function selectUsername(response) {
		if(response.data) {
			var userlist = [];
			angular.forEach(response.data, function(user, key) {
				userlist.push(user.name);
			})

			return userlist;
		}
	}

	function addUserGroup(params) {
		return BaseService.POST(url, params);
	}
}])

module.exports = userinfoservice;