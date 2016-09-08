/**
 * date format directive
 */

const dateFormat = function($filter, $rootScope) {
    //引用ng内置datefilter过滤器
    var dateFilter = $filter('date');
    return {
        require: 'ngModel',
        link: function(scope, elem, attrs, ctrl) {
            function formatter(value) {
                return dateFilter(value, 'yyyy-mm-dd');
            }

            function parser(value) {
                return dateFilter(value, 'yyyy-mm-dd');
            }

            ctrl.$parsers.push(parser);
            //ctrl.$formatters.push(formatter);
        }
    }
}

dateFormat.$inject = ['$filter', '$rootScope'];
module.exports = dateFormat;