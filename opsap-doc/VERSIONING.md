# 版本管理 #

----------

## 项目名命名规范  ##
- 全部用小写字母
- 横杠[-]作为连接字符
- 命名规则：[产品名称]-[项目类型]-[自定义名称]，自定义名称可选

举例：
osinstall-doc
osinstall-ui

实践建议：
在创建项目仓库时就要权衡前后端或者大的功能模块的拆分，保持低耦合度。
## 目录结构 ##
规范的目录结构不仅有利于开发者理解代码结构，更有利于代码的快速部署，目录结构建议将环境配置文件、日志文件，其他文件缓存等独立于代码库之外存放。开发目录应该包含但不限于以下目录：

    [root@localhost ~]# tree opsap/
    opsap/              产品名
    ├── ChangeLog.md    update change log
    ├── LICENSE         add license
    ├── opsap-django    项目名
    │   ├── dist        经过压缩合并等最终生成的代码目录
    │   ├── README.md   说明文档
    │   ├── src         源码目录
    │   └── tests       测试用例目录
    ├── opsap-doc       项目名
    │   ├── api         子目录
    │   ├── environment 子目录
    │   ├── logo.png    子目录
    │   ├── preface     子目录
    │   ├── README.md   说明文档
    │   └── SUMMARY.md  目录入口
    └── README.md       依赖、安装、部署、文档等说明

## 分支管理策略 ##

![](http://i.imgur.com/VTNkq81.png)
如上图所示：
- 最稳定的代码放在master分支上，我们不要直接在 master 分支上提交代码，只能在该分支上进行代码合并操作，例如将其它分支的代码合并到 master分支上，由版本管理员管理，普通用户不可以修改。
- 我们日常开发中的使用另一条主分支develop分支，该分支所有人都能访问，但一般情况下，我们也不会直接在该分支上提交代码，代码同样是从其它分支合并到develop分支上去。
- 当我们需要开发某个特性时，需要从develop分支拉出一条feature分支，例如feature-1与feature-2，在这些分支上并行地开发具体特性。
- 当特性开发完毕后，我们决定需要发布某个版本了，此时需要从develop分支上拉出一条 release 分支，例如 release-1.0.0，并将需要发布的特性从相关feature分支一同合并到release分支上，随后将针对release分支部署测试环境，测试工程师在该分支上做功能测试，开发工程师在该分支上修改 bug。待测试工程师无法找到任何 bug 时，我们可将该release分支部署到预发环境，再次验证以后，均无任何 bug，此时可将 release 分支部署到生产环境。
- 待上线完成后，将release分支上的代码同时合并到develop分支与master分支，并在master分支上打一个tag，例如v1.0.0。
- 当生产环境发现bug时，我们需要从对应的tag上（例如 v1.0.0）拉出一条 hotfix 分支（例如 hotfix-1.0.1），并在该分支上做 bug 修复。待bug完全修复后，需将hotfix分支上的代码同时合并到develop分支与master分支。
- 对于版本号要求格式为：x.y.z，其中，x用于有重大重构时才会升级，y用于有新的特性发布时才会升级，z用于修改了某个bug后才会升级。


