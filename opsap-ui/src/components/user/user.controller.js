/**
 * usercontroller
 */

const $inject = ['$scope', '$rootScope', '$stateParams', '$state', '$window', 'UserManagementService', 'SelectService'];
const UserController = function($scope, $rootScope,  $stateParams, $state, $window, UserManagementService, SelectService) {
	var vm = this;
	vm.userForm = {};
    vm.username = '';
    //mock data
    vm.userRole = [{value: 1, content: '普通用户'}, {value: 2, content: '管理员'}];
	vm.userGroup = ['test', 'jhhh'];
    
    vm.totalItems = 3;
    vm.currentPage = 1;
	vm.selected = [];
	vm.setSelectAll = SelectService.setSelectAll;
	vm.updateSelection = SelectService.updateSelection;
	vm.deleteUser = deleteUser;
	$scope.$on('notice', function(event, text) {
		vm.noticeMsg = text;
	})
	if($stateParams.operation === 'list') {
		UserManagementService.getUsers().then(function(result) {
			if(result.data) {
				vm.users = result.data;
				$rootScope.$broadcast('notice', 'success');
			}
		})
	} 

	function submitForm(params){
		UserManagementService.addUser(params).then(function(result) {
			if(result.status) {
				$rootScope.$broadcast('notice', '添加用户成功');
				$timeout(function() {
					$state.go('index.user', {operation:'list'});
				}, 1000);
			}
		})
	}

	function deleteUser(id, name) {
		if($window.confirm('确定删除' + name + '?')) {
			UserManagementService.deleteUser(id).then(function(result) {
				$rootScope.$broadcast('notice', '删除用户成功');
				$timeout(function() {
					$state.go('index.user', {operation:'list'});
				}, 1000);
			})
		}
	}
}
 UserController.$inject = $inject;
 module.exports = UserController;