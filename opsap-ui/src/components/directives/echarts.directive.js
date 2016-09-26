/**
 * common directive for slider
 */
let echarts = require('echarts');
const mockData = [{time:'2016-08-09', volume:32},{time:'2016-08-10', volume:20},{time:'2016-08-11', volume:22},{time:'2016-08-12', volume:23}]


function spliteData(rawdata) {
	var categorydata = [];
	var volumes = [];
	for(var i = 0, len = rawdata.length; i < len; i++) {
		categorydata.push(rawdata[i].time || '');
		volumes.push(rawdata[i].volume || 0);
	}
	return {
		categoryData: categorydata,
		volumns: volumes
	}
}
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
			var data = spliteData(mockData);
		var dataOption = {
	    title: {text: '备份数据走势图'},
        backgroundColor: '#eee',
        animation: false,
        legend: {
            bottom: 10,
            left: 'center',
            data: ['MA5', 'MA10', 'MA20', 'MA30']
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'line'
            }
        },
        toolbox: {
            feature: {
                dataZoom: {
                    yAxisIndex: false
                },
                brush: {
                    type: ['lineX', 'clear']
                }
            }
        },
        brush: {
            xAxisIndex: 'all',
            brushLink: 'all',
            outOfBrush: {
                colorAlpha: 0.1
            }
        },
        grid: [
            {
                left: '10%',
                right: '8%',
                height: '50%'
            },
            {
                left: '10%',
                right: '8%',
                top: '63%',
                height: '16%'
            }
        ],
        xAxis: [
            {
                type: 'category',
                data: data.categoryData,
                scale: true,
                boundaryGap : false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax'
            },
            {
                type: 'category',
                gridIndex: 1,
                data: data.categoryData,
                scale: true,
                boundaryGap : false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                splitNumber: 20,
                min: 'dataMin',
                max: 'dataMax'
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {
                    show: true
                }
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false}
            }
        ],
        dataZoom: [
            {
                type: 'inside',
                xAxisIndex: [0, 1],
                start: 98,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0, 1],
                type: 'slider',
                top: '85%',
                start: 98,
                end: 100
            }
        ],
        series: [
            {
                name: 'MA5',
                type: 'line',
                data: data.volumns,
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA10',
                type: 'line',
                data: data.volumns,
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA20',
                type: 'line',
                data: data.volumns,
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'MA30',
                type: 'line',
                data: data.volumns,
                smooth: true,
                lineStyle: {
                    normal: {opacity: 0.5}
                }
            },
            {
                name: 'Volumn',
                type: 'bar',
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data.volumns
            }
        ]
    };
		  myChart.setOption(dataOption);
		   myChart.dispatchAction({
        type: 'brush',
        areas: [
            {
                brushType: 'lineX',
                coordRange: ['2016-08-10', '2016-08-12'],
                xAxisIndex: 0
            }
        ]
    });
		}
	}
}

echartDirective.$inject = [];

module.exports = echartDirective;