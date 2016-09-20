/**
 * common directive for slider
 */
let echarts = require('echarts');

const echartDirective = function(){
	return {
		restrict: 'AE',
		replace: true,
		link: function($scope, $element, $attr) {
			console.log($element);
	      var mainDiv = $element[0];
		  var myChart = echarts.init(mainDiv);
		  myChart.setOption({
			  title: {text: 'EChart exm'},
			  tooltip: {},
			  xAxis: {
				  data: ['tshirt', 'jouser', 'socks']
			  },
			  yAxis: {},
			  series: [{
				  name: 'selse',
				  type: 'bar',
				  data: [4, 9, 80]
			  }]
		  });
		}
	}
}

echartDirective.$inject = [];

module.exports = echartDirective;