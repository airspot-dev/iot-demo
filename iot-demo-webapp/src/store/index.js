import Vue from 'vue'
import Vuex from 'vuex'

// Modules.
import notifications from './modules/notifications'

// Use Vuex.
Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    notifications
  }
})

export default store
