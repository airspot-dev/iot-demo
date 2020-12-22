import Vue from 'vue'
import App from './App'
import pusherService from './services/pusherService'
import store from './store'
import { BootstrapVue } from 'bootstrap-vue'
import LoadScript from 'vue-plugin-load-script'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(LoadScript)

Vue.use(pusherService, {
  store
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  store
})
