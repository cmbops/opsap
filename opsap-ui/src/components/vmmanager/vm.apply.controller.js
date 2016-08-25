
const VmApllyController = function($scope, $rootScope, $state, OptionService) {
	var vm = this;
	vm.ApplyForm = {};
	vm.ApplyForm.fun_type = 'normal';
	vm.ApplyForm.env_type = '选择';
	vm.ApplyForm.OS_type = '选择';
	vm.ApplyForm.amount = 1;
	vm.ApplyForm.dataVolume = 0;
	vm.envLabels = [];
	vm.OsLabels = [];
	vm.selectEnvtype = selectEnvtype;
	vm.selectOstype =  selectOstype;
	//vm.softwares = ['WAS 7', 'WAS 8', 'ORACLE 11', 'TOMCAT', 'NGINX'];
	vm.softwares = {WAS7: 10, WAS8: 15, ORACLE: 15, TOMCAT: 10, NGINX: 10}
	vm.changeVolume = changeVolume;
	vm.basevolume = 0;
	vm.volumeslider = {
		options: {
			floor: 0,
			ceil: 100
		}
	}
	//vm.submitForm = submitForm;
	activeFunOption();
	activeOsOption();

    $scope.$watch('vmapply.basevolume', function(ov, nv) {
    	vm.volumeslider.options.floor = vm.basevolume;
    	vm.ApplyForm.dataVolume = vm.basevolume;
    })
	$scope.$watch('vmapply.ApplyForm.fun_type', function(oldVal, newVal) {
		if(oldVal !== newVal) {
			if( newVal === 'normal') {
				vm.ApplyForm.cpu = 2;
				vm.ApplyForm.memory = 4;
			} else if( newVal === 'was') {
				vm.ApplyForm.cpu = 4;
				vm.ApplyForm.memory = 8;
			} else {
				vm.ApplyForm.cpu = 4;
				vm.ApplyForm.memory = 16;
			}
		}
		console.log(vm.ApplyForm.cpu );
	})

	function changeVolume(event, volume) {
		var checkbox = event.target;
		console.log(volume);
		var action = checkbox.checked ? 'add' : 'sub';
		updateBaseVolume(action, volume);
	}

	function updateBaseVolume(action, volume) {
		if(action == 'add') {
			vm.basevolume += volume
		} 
		if(action == 'sub') {
			vm.basevolume -= volume
		}
	}

	function activeFunOption(){
		OptionService.getOption('fun_type').then(function(data) {
		vm.envLabels = data;
		return vm.envLabels;
	});
	}
	
	function activeOsOption(){
		OptionService.getOption('OS').then(function(data) {
		vm.OsLabels = data;
		return vm.OsLabels;
	});
	}
	
	function selectEnvtype(option) {
		vm.ApplyForm.env_type = option;
	}

	function selectOstype(option) {
		vm.ApplyForm.OS_type = option;
	}
    
    //提交申请表单
	/*function submitForm(formdata) {
		VMService.setNewApply(formdata).then(function(result){
			if(result.status) {
				$timeout(function(){
					$rootScope.$broadcast('alert', '提交成功！');
					$state.go('index.vmmanager', {operation:'list'})
				}, 1000);
			}
		})
	}*/
}

VmApllyController.$inject = ['$scope', '$rootScope', '$state', 'OptionService'];

module.exports = VmApllyController;