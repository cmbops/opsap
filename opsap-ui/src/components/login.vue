<template>
  <div class="hello">
    <h2 v-if="state">{{msg}}</h2>
            <form class="m-t" role="form" method="post" action="">
                <div class="form-group">
                    <input type="text" v-model="username" class="form-control" placeholder="Username" required="length[6~50]">
                </div>
                <div class="form-group">
                    <input type="password" v-model="password" class="form-control" placeholder="Password" required="">
                </div>
                <button type="submit" class="btn btn-success block full-width m-b">Login</button>

            </form>
            <p class="m-t"> <small><b>Copyright</b> CMB DevOps team © 2016-2016</small> </p>
  </div>
</template>

<script>
// 登录页面组件
export default {
  data () {
    let title = '华商自动化运维平台'
    return {
      // note: changing this line won't causes changes
      // with hot-reload because the reloaded component
      // preserves its current state and we are modifying
      // its initial state.
      msg: title,
      state: true
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
