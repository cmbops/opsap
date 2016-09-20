/**
 * datamanagercontroller
 */

const $inject = ['$scope', '$rootScope', '$stateParams', '$state', '$window', '$filter', 'BackupdataService'];
const DatamanagerController = function($scope, $rootScope,  $stateParams, $state, $window, $filter, BackupdataService) {
	
  var vm = this;
  var dateFilter = $filter('date');
  vm.files = [{name:'opics', desc:'opics文件'}, {name:'dzda', desc:'电子档案'}];
  
  vm.selectForm = {};
  vm.enddate = new Date();
  vm.selectForm.filename = vm.files[0].name;
  vm.selectForm.filestatus = 'exits';
  vm.selectForm.emc = 'CGM';
  vm.searchForm = searchForm;
  // vm.exportExcel = exportExcel;

  // function exportExcel() {
  //   BackupdataService.getBackupData
  //     .then(function(result) {
  //       var anchor = angular.element('<a/>');
  //       anchor.attr({
  //         href: 'data:attachment/xlsx;charset=utf-8,' + encodeURI(result.data),
  //         target: '_blank'
  //       })[0].click();
  //   })
  // }
  
  $scope.$watch('datactrl.startdate', function(nV, oV) {
    vm.selectForm.startdate = nV ? dateFilter(nV, 'yyyy-MM-dd') : new Date();
  })

  $scope.$watch('datactrl.enddate', function(nV, oV) {
    vm.selectForm.enddate = dateFilter(nV, 'yyyy-MM-dd');
  })
 

  function searchForm(form) {
    BackupdataService.getBackupData.then(function(result) {
      vm.backupdatas = result;
    })
  }

  $scope.inlineOptions = {
    customClass: getDayClass,
    minDate: new Date(),
    showWeeks: true
  };

  $scope.dateOptions = {
    dateDisabled: disabled,
    formatYear: 'yy',
    maxDate: new Date(2020, 5, 22),
    minDate: new Date(),
    startingDay: 1
  };

  // Disable weekend selection
  function disabled(data) {
    var date = data.date,
      mode = data.mode;
    return mode === 'day' && (date.valueOf() > new Date().valueOf());
  }

  $scope.toggleMin = function() {
    $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
    $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
  };

  $scope.toggleMin();

  $scope.open1 = function() {
    $scope.popup1.opened = true;
  };

  $scope.open2 = function() {
    $scope.popup2.opened = true;
  };

  $scope.setDate = function(year, month, day) {
    $scope.enddate = new Date(year, month, day);
  };

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[0];
  $scope.altInputFormats = ['M!/d!/yyyy'];

  $scope.popup1 = {
    opened: false
  };

  $scope.popup2 = {
    opened: false
  };

  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date();
  afterTomorrow.setDate(tomorrow.getDate() + 1);
  $scope.events = [
    {
      date: tomorrow,
      status: 'full'
    },
    {
      date: afterTomorrow,
      status: 'partially'
    }
  ];

  function getDayClass(data) {
    var date = data.date,
      mode = data.mode;
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i = 0; i < $scope.events.length; i++) {
        var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return $scope.events[i].status;
        }
      }
    }

    return '';
  }
}
 DatamanagerController.$inject = $inject;
 module.exports = DatamanagerController;