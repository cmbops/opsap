/**
 * controller of v verify
 * 用于控制审核
 */

const VmVerifyController = function($scope, $rootScope, $uibModal, $log, $transclude, VMService) {
	var vm = this;
	vm.open = open;
	vm.titles = ['申请单号', '申请人', '申请信息', '数量', '原因', '环境类型', '处理'];
	vm.contents = [{id:1, w:'caijb', r:'2CPU/4C/40G-WAS7', f:5, g:'营改增', t:'开发环境'},{id:2, w:'caijb', r:'2CPU/4C/40G-WAS7', f:5, g:'营改增', t:'开发环境'}];
	vm.operate = true;
	vm.totalItems = 2;
    vm.currentPage = 1;
	vm.open = open;
	vm.turnback = turnback; 
	  $scope.dynamicPopover = {
    content: 'Hello, World!',
    templateUrl: './modal/vm.popoverTemplate.html',
    title: 'Title'
  };
	vm.pageChanged = function() {
    $log.log('Page changed to: ' + $scope.currentPage);
  };

	function open(size, id) {
		var modalInstance = $uibModal.open({
			size: size,
			template: require('./modal/vm.agree.modal.html'),
			controller: 'VerifyModalController',
			controllerAs: 'verifymodal',
			resolve: {
				contents: function() {
					var _tempdata = [];
					console.log(id);
					return VMService.getVmResource(id).then(function (result) {
						if(result.data) {
							_tempdata = result.data
							return _tempdata;
						}
					})
				},
				id: function() {
					return id;
				} 
			}
		})

		modalInstance.result.then(function (data) {
			$log.info(data);
		}, function () {
			$log.info('Modal dismiss at' + new Date());
		});
	}

	function turnback(id) {
		var returnbackModalInstance = $uibModal.open({
			animation: true,
			template: require('./modal/vm.turnback.modal.html'),
			controller: 'TurnbackController',
			controllerAs: '$tbctrl',
			resolve: {
				id: function() {
					return id;
				}
			}
		})
	}
}

VmVerifyController.$inject = ['$scope', '$rootScope', '$uibModal', '$log', '$transclude', 'VMService'];

module.exports = VmVerifyController;