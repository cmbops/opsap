/**
 * common directive for slider
 */
let echarts = require('echarts');

const echartDirective = function(){
	return {
		restrict: 'AE',
		replace: true,
		scope: {
			title: '=',
			getdata: '&'
		},
		link: function($scope, $element, $attr) {
		  var xData = $scope.getdata(),
		      yData = $scope.getdata();
	      var mainDiv = $element[0];
		  var myChart = echarts.init(mainDiv);
		  var option =  {
			      title: {text: 'EChart exm'},
			      tooltip: {},
			      xAxis: {
			    	  data: xData
			      },
			      yAxis: {},
			      series: [{
			    	  name: 'selse',
			    	  type: 'bar',
			    	  data: yData
			      }]
				};
		//   myChart.showLoading();
		//   $scope.getdata()
		//     .then(function(result) {
		// 		angular.forEach(result.data, function(data, index) {
		// 			xData.push(data.id);
		// 			yData.push(data.dataVolume);
		// 		});
		// 		option = {
		// 	      title: {text: 'EChart exm'},
		// 	      tooltip: {},
		// 	      xAxis: {
		// 	    	  data: xData
		// 	      },
		// 	      yAxis: {},
		// 	      series: [{
		// 	    	  name: 'selse',
		// 	    	  type: 'bar',
		// 	    	  data: yData
		// 	      }]
		// 		}
		// 		myChart.hideLoading();
		// 	}).catch(function(err) {
		// 		console.log(err);
		// 	})
		  myChart.setOption(option);
		}
	}
}

echartDirective.$inject = [];

module.exports = echartDirective;