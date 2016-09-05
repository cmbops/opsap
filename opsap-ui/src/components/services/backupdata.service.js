/**
 * service for backupdata
 */

require('../../baseService');

var api = require('../../apiurl.js');

var bacupdataservice = angular.module('backupdataService', ['baseService']);

bacupdataservice.factory('BackupdataService', ['$rootScope', 'BaseService', function($rootScope, BaseService){
	var _backpupdatamanage = {
		getBackupData: getBackupData
	}
	return _backpupdatamanage;

	function getBackupData(param) {
		return BaseService.POST( api.datamanage.post_datasource_list, param).then(function(result) {
			return result.data || {};
		});
	} 

}]);

module.exports = bacupdataservice;