/**
 * api-url
 */

const DOMAIN_URL = 'http://118.240.29.16';

module.exports = {
	user: {
		post_add_user: DOMAIN_URL + 'ouser/user/add/',
		post_edit_user: DOMAIN_URL + 'ouser/user/edit',
		post_delete_user: DOMAIN_URL + 'ouser/user/delete',
		get_list_users: DOMAIN_URL + 'ouser/user/list'
	},  
	usergroup: {
		post_add_usergroup: DOMAIN_URL + 'ouser/group/add',
		post_edit_usergroup: DOMAIN_URL + 'ouser/group/edit',
		post_delete_usergroup: DOMAIN_URL + 'ouser/group/delete',
		get_list_usergroups: DOMAIN_URL + 'ouser/group/list' 
	},
	vmresource: {
		append_order: DOMAIN_URL + 'ovm/order/append', //"approval_id, apply_cpu, apply_memory_gb, "apply_datadisk_gb, "apply_os_version, "apply_softwares, apply_num
		prepare_order_resource: DOMAIN_URL + 'ovm/order/prepare', //id, vmorder主键 , 分割列表
		gen_order_resource: DOMAIN_URL + 'ovm/order/gen', //approval_id ‘,’分割
		list_order_resource: DOMAIN_URL + 'ovm/order/list', //approval_id
	},
	datamanage: {
		get_app_list: DOMAIN_URL + 'odata/app/list', //
		get_calendar: DOMAIN_URL + 'odata/calendar/list', //
		get_datasource_list: DOMAIN_URL + 'odata/datasource/list',
		get_format_daily: DOMAIN_URL + 'odata/format/daily', //post yyyy-mm-dd,
		get_format_size: DOMAIN_URL + 'odata/format/size', //yyyy,yyyy-mm,yyyy-mm-dd,ALL [,隔开]
	}
}