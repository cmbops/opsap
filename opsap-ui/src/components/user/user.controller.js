/**
 * usercontroller
 */

const $inject = ['$scope', '$rootScope', '$stateParams', '$state', 'UserManagementService'];
const UserController = function($scope, $rootScope,  $stateParams, $state, UserManagementService) {
	var vm = this;
    vm.username = '';
	$scope.$on('notice', function() {
		vm.successShow = 'wow';
	})
	if($stateParams.operation === 'list') {
		UserManagementService.getUsers().then(function(result) {
			if(result.data) {
				vm.users = result.data;
				console.log($scope.users);
				$rootScope.$broadcast('notice', 'success');
			}
		})
	}
}
 UserController.$inject = $inject;
 module.exports = UserController;