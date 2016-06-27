import { router } from '../main'

var store = require('storejs')
// 本地测试使用，使用NGINX需改变url指向
const API_URL = 'http://localhost:3001'

export default {
  user: {
    authoenticated: false
  },
  login (context, creds, redirect) {
    var url = API_URL + '/sessions/create'

    context.$http.post(url, creds)
      .then((res) => {
        store.set('id_token', res.data.id_token)
        this.user.authoenticated = true
        console.log(res.data.id_token)
        if (redirect) {
          router.go(redirect)
        }
      })
      .catch((err) => {
        console.log(err)
        context.error = err.data
      })
  },
  logout () {
    store.remove('id_token')
    this.user.authoenticated = false
  },
  check () {
    var jwt = store.get('id_token')
    if (jwt) {
      this.user.authoenticated = true
    } else {
      this.user.authoenticated = false
    }
  },
  getAuthHeader () {
    return {
      'Authorization': 'Bearer ' + store.get('id_token')
    }
  }
}
