/**
 * controller of verify returnback modal
 * 用于控制回退模态框
 */

const VerifyReturnbackModalController = function($scope, $rootScope, $uibModalInstance, $timeout, VMService, id) {
	var vm = this;
	vm.id = id;
	vm.submitReturnback = submitReturnback;
	vm.cancel = cancel;
    $scope.$on('notice', function(event, text) {
        vm.noticeMsg = text;
    })

	function submitReturnback(id) {
		VMService.SetReturnback(id).then( function(result) {
			if(result.data) {
				$rootScope.$brocast('notice', 'submit success');
                $timeout(function() {
                    $uibModalInstance.close(id)
                }, 1000)
			}
			
		})
	}

	function cancel() {
		$uibModalInstance.close('cancel');
	}
}

VerifyReturnbackModalController.$inject = ['$scope', '$rootScope', '$uibModalInstance','$timeout', 'VMService', 'id'];

module.exports = VerifyReturnbackModalController;