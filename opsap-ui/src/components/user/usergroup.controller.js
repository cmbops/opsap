/**
 * usergroupcontroller of opsap.user
 */

const $inject = ['$scope', '$rootScope', '$state'];
const UserGroupController = function($scope, $rootScope, $state) {
	$scope.test = "test"
}

UserGroupController.$inject = $inject;
module.exports = UserGroupController;