const namespaced = true

const state = {
  notifications: [],
  devices: []
}

const getters = {
  getNotifications: state => {
    return state.notifications
  },
  getDevices: state => {
    return state.devices
  },
  getNotificationsCount: state => {
    if (!state.notifications) {
      return 0
    }
    return state.notifications.length
  }
}

const mutations = {
  changeNotifications: (state, data) => {
    console.log(data)
    try {
      if (data.device) {
        if (data.payload.event) {
          state.notifications.push(data.device + ': ' + data.payload.event)
        } else {
          state.notifications.push('New value for ' + data.device + ': ' + data.payload.value)
        }
        for (var d in state.devices) {
          var dev = state.devices[d]
          if (dev) {
            console.log(data.device)
            if (dev.id === data.device) {
              for (var k in data.payload) {
                dev[k] = data.payload[k]
              }
              return
            }
          }
        }
        var newDevice = data.payload
        newDevice['id'] = data.device
        state.devices.push(newDevice)
        console.log(state.devices)
        console.log(state.notifications)
      }
    } catch (err) {
      console.log(err)
      state.notifications.push(data)
    }
  }
}

const actions = {
  setNotifications: ({commit}, payload) => {
    commit('changeNotifications', payload)
  }
}

export default {
  namespaced,
  state,
  getters,
  mutations,
  actions
}
