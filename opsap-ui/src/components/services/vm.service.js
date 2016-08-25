/**
 * userinfo service
 */
require('../../baseService');


var COMMON_URL = ''
var vmservice = angular.module('vmService', ['baseService']);

vmservice.factory('VMService', ['$rootScope', 'BaseService', function($rootScope, BaseService){
	var vmmanagement = {
		getVmResource: getVmResource,
		setNewApply: setNewApply,
		SetNewVerify: SetNewVerify,
		SetNewGenerate:  SetNewGenerate
	}

	return vmmanagement;

	function setNewApply(param){
		return BaseService.POST( COMMON_URL + '/vmapply', param);
	}

	function getVmResource(id) {
		return BaseService.GET('../src/components/data/vmresource.json');
	}

	function SetNewVerify(id) {
		return BaseService.POST( COMMON_URL + '/veify', {id: id});
	}

	function SetNewGenerate(selected) {
		return BaseService.POST( COMMON_URL + '/generate', {ids: selected});
	}

}])

module.exports = vmservice;