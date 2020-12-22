<template>
  <div id="app">
    <Dashboard/>
  </div>
</template>

<script>
import Dashboard from './components/Dashboard'
var $ = require('jquery')
window.jQuery = $

export default {
  name: 'App',
  components: {
    Dashboard
  }
}
</script>

<style lang="scss">
@import './assets/vendor/bootstrap/css/bootstrap.min.css';
</style>

<style lang="scss">
@import './assets/vendor/font-awesome/css/font-awesome.min.css';
</style>
<style lang="scss">
@import './assets/vendor/linearicons/style.css';
</style>
<style lang="scss">
@import './assets/vendor/chartist/css/chartist-custom.css';
</style>
<style lang="scss">
@import './assets/css/main.css';
</style>
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
