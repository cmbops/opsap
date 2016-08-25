/**
 * setting service
 */
require('../../baseService');

var settingservice = angular.module('settingService', ['baseService']);

settingservice.factory('OptionService', ['$rootScope', 'BaseService', function($rootScope, BaseService){
	var option = {
		getOption: getOption
	}
	return option;
     
    //获取选项
	function getOption(option) {
		return  BaseService.GET('../src/components/data/option.json').then(getOptionComplete);
		
		function getOptionComplete(response) {
			if(response.data) {
				var options = [];
				angular.forEach(response.data, function(res, key) {
					if(res.name === option) {
						angular.copy(res.group, options);
					}
				});
				console.log(options);
				return options;
			}
		}
	}
}])