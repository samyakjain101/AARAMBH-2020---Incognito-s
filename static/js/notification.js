console.log('Notification');

const notificationSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/notify/'
    + JSON.parse(document.getElementById('notify-room-name').textContent)
    + '/'
);

notificationSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data.message);
    document.getElementById('notification').innerHTML = data.message;
};

notificationSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};