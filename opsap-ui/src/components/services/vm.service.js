/**
 * userinfo service
 */
require('../../baseService');


var COMMON_URL = require('../../apiurl.js');
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
		return BaseService.POST( COMMON_URL.vmresource.prepare_order_resource, {ids: selected});
	}

}])

module.exports = vmservice;