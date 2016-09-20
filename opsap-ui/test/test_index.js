/**
 * index test file for webpack
 */
require('angular');
require('angular-mocks/angular-mocks');

var testsContext = require.context(".", true, /_test$/);
testsContext.keys().forEach(testsContext);