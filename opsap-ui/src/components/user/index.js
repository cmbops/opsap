/**
 * module opsap.user
 */
require('../../baseService');
require('../services/userinfo.service')

module.exports = angular.module('opsap.user', ['userinfoService', 'baseService'])
                   .controller('UserController', require('./user.controller'))
                   .controller('UserGroupController', require('./usergroup.controller'));