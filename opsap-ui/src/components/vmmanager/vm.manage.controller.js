
const VmManageController = function($scope, $rootScope, $state, $stateParams, $sce, $interval, SelectService, VMService) {
	var vm = this;
	vm.resourcelist = [{id:1, appro_os_type:'WIN', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', process:0, gen_log: 'success'},
	               {id:2, appro_os_type:'LUX', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', process:80, gen_log: 'success'},
	               {id:3, appro_os_type:'SUSE', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', process:100, gen_log: 'success'}];
    vm.selected = [];
    vm.isSelected = SelectService.isSelected;
    vm.setSelectAll = SelectService.setSelectAll;
    vm.updateSelection = SelectService.updateSelection;
    vm.generateResource = generateResource;
    vm.loading = false;
	vm.dynamicPopover = {
    content: 'Hello, World!',
    title: 'Title'
  };
    vm.dynamicHtml = $sce.trustAsHtml(require('./modal/vm.popoverTemplate.html'));

    function generateResource(selected) {
            vm.resourcelist.push({id:4, appro_os_type:'SUSE', ipaddress:'192.168.7.2', loc_cluster_name: 'hGff5d', loc_storage_name: 'Yifdf', process:100, gen_log: 'success'});
    }
}

VmManageController.$inject = ['$scope', '$rootScope', '$state', '$stateParams', '$sce', '$interval', 'SelectService', 'VMService'];

module.exports = VmManageController;