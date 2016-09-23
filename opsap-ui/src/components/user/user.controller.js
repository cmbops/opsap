/**
 * usercontroller
 */

const $inject = ['$scope', '$rootScope', '$stateParams', '$state', '$window', '$timeout', 'UserManagementService', 'SelectService'];
const UserController = function($scope, $rootScope,  $stateParams, $state, $window, $timeout, UserManagementService, SelectService) {
	var vm = this;
	vm.userForm = {};
    vm.username = '';
    //mock data
    vm.userRole = [{value: 1, content: '普通用户'}, {value: 2, content: '管理员'}];
	vm.userGroup = ['test', 'jhhh'];
    
    vm.totalItems = 100;
    vm.currentPage = 1;
	vm.pageChanged = function() {
		console.log(vm.currentPage);
	}
	vm.selected = [];
	vm.isSelected = SelectService.isSelected;
	vm.setSelectAll = SelectService.setSelectAll;
	vm.updateSelection = SelectService.updateSelection;
	vm.deleteUser = deleteUser;
	vm.loading = true;
	$scope.$on('notice', function(event, text) {
		vm.noticeMsg = text;
	})
	if($stateParams.operation === 'list') {
		UserManagementService.getUsers().then(function(result) {
			if(result.data) {
				$timeout(function() {
					vm.loading = false;
				vm.users = result.data;
				$rootScope.$broadcast('notice', 'success');
				}, 2000);
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