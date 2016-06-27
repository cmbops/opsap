<template>
  <div class="hello">
    <img class="logo" src="../assets/logo.png">
    <h2 v-if="state">华商自动化运维平台</h2>
            <form class="m-t" role="form" method="post" action="">
                <div class="form-group">
                    <input type="text" v-model="credentials.username"  class="form-control" placeholder="Username" required="length[6~50]">
                </div>
                <div class="form-group">
                    <input type="password" v-model="credentials.password" class="form-control" placeholder="Password" required="">
                </div>
                <button @click="submit" class="btn btn-success block full-width m-b">Login</button>
                
            </form>
            <div class="alert alert-danger" v-if="error">{{error}}</div>
            <p class="m-t"> <small><b>Copyright</b> CMB DevOps team © 2016-2016</small> </p>
  </div>
</template>

<script>
import auth from '../auth'
// 登录页面组件
export default {
  data () {
    console.log(auth.user.authoenticated)
    return {
      credentials: {
        username: '',
        password: ''
      },
      error: ''
    }
  },
  methods: {
    submit () {
      var credentials = {
        username: this.credentials.username,
        password: this.credentials.password
      }
      auth.login(this, credentials, 'index')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  color: #42b983;
}

.full-width {
  width: 100%;
}

.loginscreen.middle-box {
  width: 300px;
  margin-left: -150px;
  margin-top: -330px;
}

.middle-box {
  height: 400px;
  width: 400px;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -250px;
  margin-left: -200px;
  z-index: 100;
}
.middle-box h1 {
  font-size: 170px;
}

.logo-name {
  color: #e6e6e6;
  font-size: 180px;
  font-weight: 800;
  letter-spacing: -10px;
  margin-bottom: 0px;
}
</style>
