## OPSAP前端介绍
结合华商运维平台需求及公司的技术栈，本平台前端用到的技术主要有：bootstrap UI框架，angularJS 框架，webpack打包模块管理工具以及karma单元测试工具。由于bootstrap及angular的限制，本平台仅支持IE8以上浏览器。

### bootstrap UI框架
平台采用目前流行的twitter公司开源UI框架bootstrap 3，Bootstrap 是基于 HTML、CSS、JAVASCRIPT 的，它简洁灵活，使得 Web 开发更加快捷，bootstrap提供了各种布局组件及插件帮助我们完成界面的开发。

### angularJS 框架
angularJS是一款优秀的前端JS框架，AngularJS有着诸多特性，最为核心的是：MVVM、模块化、自动化双向数据绑定、语义化标签、依赖注入等等，这些特性使得我们在构建一个CRUD（增加Create、查询Retrieve、更新Update、删除Delete）的应用时非常方便。本平台在angular style guide(angular编程规范)的指引以及webpack模块管理工具的帮助下，实现了部件开发，不同的部件有相对应的module(模块)及相关的controller(控制器)，共享directive(组件)及service(服务), 一个部件作为平台一个单元进行单独开发。
![alt opsap-code-org](/Users/darsycheuk/Desktop/opsap/opsap-ui/src/assets/img/opsap－structure.png)

### webpack模块打包管理工具
webpack是流行的一款模块加载器兼打包工具，它能把各种资源，例如JS（含JSX）、coffee、样式（含less/sass）、图片等都作为模块来使用和处理，借助它能实现前端工程化及代码组织模块化。

### karma & jasmine 测试
karma是angular团队推出配合angular进行自动化测试工具(测试执行器 test Runner)，jasmine是一款JS测试框架，结合karma及jasmine，可实现对angular代码的自动化单元测试。

```
describe('navbar test', function() {
    let ctrl, scope;
    describe('navbar controller test', function() {
        beforeEach(function() {
        angular.mock.module(navCtrl);

        angular.mock.inject(function($controller, $rootScope) {
            scope = $rootScope.$new();
            ctrl = $controller('NavController', {$scope: scope});
        })
    })
   //测试点
    it('should have title in NavController', function() {
        expect(ctrl.title).toBe('index');
    })    
    
    })
})

```
![opsap karma](/Users/darsycheuk/Desktop/opsap/opsap-ui/src/assets/img/opsap-spec.png)

