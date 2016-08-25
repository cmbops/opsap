/**
 * [opsap vmmanager module]
 * @type {module}
 */
require('../../baseService')
require('../services/setting.service')
require('../services/vm.service')

module.exports = angular.module('opsap.vmmanager', ['settingService', 'vmService', 'baseService'])
                   .controller('VmApllyController', require('./vm.apply.controller'))
                   .controller('VmVerifyController', require('./vm.verify.controller'))
                   .controller('VerifyModalController', require('./vm.verifymodal.controller'))
                   .controller('VmManageController', require('./vm.manage.controller'))
                   .directive('sliderBar', require('../directives/slider.directive'))
                   .directive('verifyTable', require('../directives/tablerender.directive'));