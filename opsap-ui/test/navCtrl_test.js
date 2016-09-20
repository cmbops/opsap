/**
 * spec file for nav.controller.js
 */
let navCtrl = require('../src/components/dashboard/').name;

describe('navbar test', function() {
    let ctrl, scope;
    describe('navbar controller test', function() {
        beforeEach(function() {
        angular.mock.module(navCtrl);

        angular.mock.inject(function($controller, $rootScope) {
            scope = $rootScope.$new();
            ctrl = $controller('NavController', {$scope: scope});
        })
    })
   //测试点
    it('should have title in NavController', function() {
        expect(ctrl.title).toBe('index');
    })    
    
    })
})
