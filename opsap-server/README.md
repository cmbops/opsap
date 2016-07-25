# OPSAP-RESTful API文档 #

### 接口URL ###

    http://OPSAP-SERVER服务器地址:端口/接口URI/

----------

### 如何指定数据格式(支持：browsableAPI 、 `json`) ###

a) 在url中添加`format`参数

	http://OPSAP-SERVER服务器地址:端口/接口URI/?format=json
	http://OPSAP-SERVER服务器地址:端口/接口URI/?format=api

b) 在请求头指定`Accept`标签

    Accept:application/json

----------

### API目录树 ###
	URI								请求类型				用途描述
	
	/
	/api-token-auth    				POST				获取身份认证token
	/param/
	/param/get						POST				查询系统参数
	/param/set						POST				设置系统参数
	/options/
	/options/add					POST				添加动态表单选项
	/options/list					POST				获取动态表单选项
	/options/edit					POST				修改动态表单选项
	/options/delete					POST				删除动态表单选项
	/ouser/
	/ouser/user/
	/ouser/user/add					POST				添加用户
	/ouser/user/list				GET					获取用户列表
	/ouser/user/detail				GET/POST			获取用户详情
	/ouser/user/edit				POST				修改用户信息
	/ouser/user/delete				POST				删除用户
	/ouser/group/
	/ouser/group/add				POST				添加用户组
	/ouser/group/list				GET					获取用户组列表
	/ouser/group/edit				POST				修改用户组信息
	/ouser/group/delete				POST				删除用户组
	/ovm/
	/ovm/application/
	/ovm/application/add			POST				添加VM申请
	/ovm/application/list			GET/POST			获取VM申请列表
	/ovm/application/detail			POST				获取VM申请详情
	/ovm/application/edit			POST				修改VM申请信息
	/ovm/application/submit			POST				提交VM申请
	/ovm/application/delete			POST				删除VM申请
	/ovm/approvel/
	/ovm/approvel/apply				POST				添加VM申请
	/ovm/approvel/list				GET/POST			获取VM审核列表
	/ovm/approvel/detail			POST				获取VM审核详情
	/ovm/approvel/edit				POST				修改VM审核信息
	/ovm/approvel/agree				POST				同意VM申请
	/ovm/approvel/reject			POST				驳回VM审核
	/ovm/order/
	/ovm/order/list					GET/POST			获取VM订单列表
	/ovm/order/detail				POST				获取VM订单详情
	/ovm/order/edit					POST				修改VM订单信息
	/ovm/order/generate				POST				生成VM资源
	/ovm/resource/
	/ovm/resource/vc/
	/ovm/resource/vc/add			POST				添加VCenter
	/ovm/resource/vc/list			GET/POST			获取VCenter列表
	/ovm/resource/vc/edit			POST				修改VCenter信息
	/ovm/resource/vc/sync			POST				从VCenter同步资源
	/ovm/resource/vc/delete			POST				删除VCenter
	/ovm/resource/ippool/
	/ovm/resource/ippool/init		POST				添加IP地址池
	/ovm/resource/ippool/list		GET/POST			获取IP地址池列表
	/ovm/resource/ippool/manage		POST				管理IP地址池
	/ovm/resource/templ/
	/ovm/resource/templ/add			POST				指定VM模板
	/ovm/resource/templ/list		GET/POST			获取VM模板列表
	/ovm/resource/templ/edit		POST				修改VM模板信息
	/ovm/resource/templ/delete		POST				删除VM模板关联
	...


----------

### API详细描述 ###

	待续...