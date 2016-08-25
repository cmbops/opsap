/**
 * controller of verify modal
 * 用于控制审核模态框
 */

const VerifyModalController = function($scope, $rootScope, $uibModalInstance, VMService, contents, id) {
	var vm = this;
	vm.titles = ['申请单号', '环境类型', '主机类型', 'CPU', '内存', '系统盘', '数据盘', '操作系统', 'IP', '虚拟机名', '系统名', '群集', '资源池', '存储'];
	vm.contents = contents;
	vm.operate = true;
	vm.id = id;
	vm.submitVerify = submitVerify;
	vm.cancel = cancel;

	function submitVerify(id) {
		VMService.SetNewVerify(id).then( function(result) {
			if(result.data) {
				$rootScope.$brocast('notice', 'submit success');
			}
			
		})
		$uibModalInstance.close(id)
	}

	function cancel() {
		$uibModalInstance.dismiss('cancel');
	}
}

VerifyModalController.$inject = ['$scope', '$rootScope', '$uibModalInstance', 'VMService', 'contents', 'id'];

module.exports = VerifyModalController;