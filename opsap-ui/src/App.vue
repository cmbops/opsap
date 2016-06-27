<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>


<style>
html {
  height: 100%;
}

body {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #676A6C;
  font-family: "open sans","Helvetica Neue",Helvetica,Arial,"微软雅黑",sans-serif;
}

#app {
  color: #2c3e50;
  margin-top: -100px;
  max-width: 600px;
  font-family: Source Sans Pro, Helvetica, sans-serif;
  text-align: center;
}

#app a {
  color: #42b983;
  text-decoration: none;
}


</style>
