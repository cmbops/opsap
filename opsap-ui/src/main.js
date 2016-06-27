import Vue from 'vue'
import App from './App'
import login from './components/login'
import index from './components/index'
import 'bootstrap/dist/css/bootstrap.min.css'

import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

Vue.use(VueResource)
Vue.use(VueRouter)
Vue.http.options.emulateJSON = true

export var router = new VueRouter()

// 路由
router.map({
  'login': {
    component: login
  },
  'index': {
    component: index
  }
})

router.redirect({
  '*': '/login'
})

router.start(App, '#app')
/* eslint-disable no-new */
/* new Vue({
  el: 'body',
  components: { App }
}) */
