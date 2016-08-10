/**
 * module opsap.user
 */
require('../services/userinfo.service')

module.exports = angular.module('opsap.user', ['userinfoService'])
                   .controller('UserController', require('./user.controller'))
                   .controller('UserGroupControlle', require('./usergroup.controller'));