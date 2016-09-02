/**
 * usergroupcontroller of opsap.user
 */

const $inject = ['$scope', '$rootScope', '$state', '$stateParams', 'UserManagementService'];
const UserGroupController = function($scope, $rootScope, $state, $stateParams, UserManagementService) {
	var vm = this;
	vm.groupForm = {};
	vm.move = move;
	vm.chosenuser = [];
	vm.submitNewUserGroupForm = submitNewUserGroupForm;
	vm.selected = [];
	vm.updateSelection = updateSelection;
	vm.isSelected = isSelected;
	vm.setSelectAll = setSelectAll;
	vm.deleteSelect = deleteSelect;
	activeUserList();

    if($stateParams.operation === 'list') {
		UserManagementService.getUserGroups().then(function(result) {
			if(result.data) {
				vm.usergroup = result.data;
				$rootScope.$broadcast('notice', 'success');
			}
		})
	} 
	function move(select){
		vm.groupForm.userarray = angular.copy(select);
		vm.chosenuser = angular.copy(select);
	}

	function activeUserList() {
		UserManagementService.getUserList().then(function(data) {
			vm.userlist = data;
			return vm.userlist;
		})
	}

    //提交新用户组
	function submitNewUserGroupForm(params) {
		UserManagementService.addUserGroup(params).then(function(result) {

		})
	}

	//删除选择用户组
	function deleteSelect(selected) {
		console.log(selected.join(','));
	}

	//选择删除
	function updateSelection(event, id) {
		var checkbox = event.target;
		var action = (checkbox.checked ? 'add' : 'remove');
		updateSelected(action, id);
	}

	function updateSelected(action, id) {
		if(action == 'add' && vm.selected.indexOf(id) == -1) {
			vm.selected.push(id);
		}
		if(action == 'remove' && vm.selected.indexOf(id) != -1) {
			var idx = vm.selected.indexOf(id);
			vm.selected.splice(idx, 1);
		}
	}

	function isSelected(id) {
		return vm.selected.indexOf(id)>=0;
	}

	function setSelectAll(event) {
		var checkbox = event.target;
		var action = (checkbox.checked ? 'add' : 'remove');
		for(let i = 0; i < vm.usergroup.length; i++) {
			let entity = vm.usergroup[i];
			updateSelected(action, entity.id);
		}
	}
}

UserGroupController.$inject = $inject;
module.exports = UserGroupController;