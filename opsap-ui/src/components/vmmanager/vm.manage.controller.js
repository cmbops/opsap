
const VmManageController = function($scope, $rootScope, $state, $stateParams, SelectService, VMService) {
	var vm = this;
	vm.resourcelist = [{id:1, appro_os_type:'WIN', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', gen_log: 'success'},
	               {id:2, appro_os_type:'LUX', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', gen_log: 'success'},
	               {id:3, appro_os_type:'SUSE', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', gen_log: 'success'}];
    vm.selected = [];
    vm.isSelected = SelectService.isSelected;
    vm.setSelectAll = SelectService.setSelectAll;
    vm.updateSelection = SelectService.updateSelection;
    vm.generateResource = generateResource;
	vm.dynamicPopover = {
    content: 'Hello, World!',
    templateUrl: 'myPopoverTemplate.html',
    title: 'Title'
  };

    function generateResource(selected) {
    	VMService.SetNewGenerate(selected).then(function(result) {
    		if(result.data) {
    			$rootScope.$broadcast('notice', 'success');
    		}
    	})
    }
}

VmManageController.$inject = ['$scope', '$rootScope', '$state', '$stateParams', 'SelectService', 'VMService'];

module.exports = VmManageController;