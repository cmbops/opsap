'use strict';

var loaderUtils = require('loader-utils');
var _ = require('lodash');
var isparta = require('isparta');

module.exports = function(source) {

    var query = loaderUtils.parseQuery(this.query);
    var options = _.assign({
        embedSource: true,
        noAutoWrap: true
    }, query);
    var instrumenter = new isparta.Instrumenter(options);

    if (this.cacheable) {
        this.cacheable();
    }

    return instrumenter.instrumentSync(source, this.resourcePath);
};
