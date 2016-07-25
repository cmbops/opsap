/**
 * @param  {angular.controller}
 * @param  {login}
 * @return {failed|success}
 */
module.exports = ['$scope', '$rootScope', '$state', '$window', 'UserService',  function($scope, $rootScope, $state, $window, UserService){
	$scope.user = {}
	$scope.login = function() {
		if(!$scope.user.username || !$scope.user.password) {
			$rootScope.$broadcast('alert', '账号或者密码格式错误');
			console.log($scope.user);
			return;
		}
		console.log('start..');
		UserService.login($scope.user.username, $scope.user.password).then(function(result){
			console.log(result);
			if(result.data.id_token){
				$window.sessionStorage.token = result.data.id_token;
				$state.go('index');
			} else {
				$rootScope.$broadcast('alert', '账号不存在，或者密码错误');
				console.log('error');
			}
		})
	}
	$scope.checkEnter = function($event) {
		if($event.keyCode == 13) {
			$scope.login();
		}
	}
}]