/**
 * directive for popover
 */

const popoverDirective = function($sce) {
    return {
        district: 'AE',
        replace: true,
        scope: {
            contents: '='
        },
        template: require('./popover.directive.html'),
        link: function(scope, elem, attr) {
            var HTML = '<div><button>' + scope.contents + '</button></div>';
            scope.htmlPopover = $sce.trustAsHtml(HTML);
        }
    }
}

popoverDirective.$inject = ['$sce']
module.exports = popoverDirective;
