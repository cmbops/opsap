<template>
	<div class="col-sm-3">
		<div class="ibox float-e-margins">
			<div class="ibox-title">
				<span class="label label-success pull-right">{{title}}</span>
				<h5>{{title}}</h5>
			</div>
			<div class="ibox-content">
				<h1 class="no-margins">
					<a @click="getQuote">re</a>
				</h1>
				<small>rer</small>
			</div>
		</div>
	</div>
</template>
<script>
import auth from '../auth'
export default {
  data () {
    return {
      title: ''
    }
  },
  methods: {
    getQuote () {
      this.$http.get('http://localhost:3001/api/protected/random-quote', null, { headers: auth.getAuthHeader })
        .then((res) => {
          this.title = res.data
        })
        .catch((err) => { console.log(err) })
    }
  },
  route: {
    canActivate () {
      return auth.user.authenticated
    }
  }
}
</script>