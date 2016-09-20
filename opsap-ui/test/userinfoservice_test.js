/**
 * test for userinfo.service
 */

let userinfoService = require('../src/components/services/userinfo.service.js').name;

describe('test unit for userinfo', function() {
    let responseJson = [{name: 'ds', role: 'cu'}, {name: 'cjb', role: 'su'}];
    beforeEach(() => {
        angular.mock.module(userinfoService);
    });
    it('getUsers should be 1', function() {
        angular.mock.inject(function($injector) {
        var $httpBackend = $injector.get('$httpBackend');
        $httpBackend.when('GET', '../src/components/data/user.json').respond(responseJson);
        var UserManagementService = $injector.get('UserManagementService');
        var promise = UserManagementService.getUsers();
        var userNum;
        promise.then(function(response) {
            console.log(response);
            userNum = response.data.length;
        }).catch(function(err) {
            userNum = 0;
        })
        $httpBackend.flush();

        var $rootScope = $injector.get('$rootScope');
        $rootScope.$apply();   
        expect(userNum).toBe(2);        
    })
    });
    it('getUserList should be [ds, cjb]', () => {
        angular.mock.inject(function($injector) {
        var $httpBackend = $injector.get('$httpBackend');
        $httpBackend.when('GET', '../src/components/data/user.json').respond(responseJson);
        var UserManagementService = $injector.get('UserManagementService');
        var promise = UserManagementService.getUserList();
        var userset;
        promise.then((data)=>{
            userset = data;
        })
        $httpBackend.flush();
        var $rootScope = $injector.get('$rootScope');
        $rootScope.$apply()   
        expect(userset).toEqual(['ds', 'cjb']);
        });
    });
})