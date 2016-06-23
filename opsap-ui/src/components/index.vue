<template>
	<div class="col-sm-3">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <span class="label label-success pull-right">{{title_en}}</span>
                    <h5>{{title_ch}}</h5>
                </div>
                <div class="ibox-content">
                    <h1 class="no-margins">
                        <a>{{num}}</a>
                    </h1>
                    <small>{{description}}</small>
                </div>
            </div>
        </div>
</template>
<script>
	export default {
		data: {
			title_en: 'users',
			title_ch: '全部用户',
			num: 0,
			description: 'all users'
		},
		computed: {
			num: () => this.num + 'test'
		}
	}
</script>