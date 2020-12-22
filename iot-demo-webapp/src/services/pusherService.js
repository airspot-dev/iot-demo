import Pusher from 'pusher-js'
let pusherService = {}

pusherService.install = function (Vue, options) {
  let pusher = new Pusher(process.env['PUSHER_API_KEY'], {
    cluster: 'eu'
  })
  var channel = pusher.subscribe(process.env['FLEET_CHANNEL'])
  channel.bind(process.env['DEVICES_DATA_EVENT'], function (data) {
    handleNotification(data)
  })

  /*
    Here we write our custom functions to not make a mess in one function
  */
  function handleNotification (data) {
    console.log(data)
    options.store.dispatch('notifications/setNotifications', data)
  }
}

export default pusherService
