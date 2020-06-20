<template>
  <div class="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Material+Icons");
@import url("https://cdn.bootcss.com/material-design-icons/3.0.1/iconfont/material-icons.css");
.app {
  height: 100vh;
  overflow: hidden;
}
</style>