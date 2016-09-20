/**
 * karma test
 */

const Util = require('./case');

xdescribe('index.js: ', function() {
  xit('isNum() should work fine.', function() {
    expect(Util.isNum(1)).toBe(true);
    expect(Util.isNum('1')).toBe(false);
  })
})