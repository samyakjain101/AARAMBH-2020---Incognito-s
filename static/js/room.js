console.log('working')
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const current_user = JSON.parse(document.getElementById('current-user').textContent);
const current_user_pic = document.getElementById('profile-img').getAttribute('src');
const user2_pic = document.getElementById('contact-profile-img').getAttribute('src');

const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data.message)
    if (data.author) {
        if (data.author === current_user) {
            $(".messages ul").append('<li class="sent"> <img src="' + current_user_pic + '" alt="" /> <p>' + data.message + '</p> </li>');
        } else {
            $(".messages ul").append('<li class="replies"> <img src="' + user2_pic + '" alt="" /> <p>' + data.message + '</p> </li>');
        }
    }
    $(".messages").animate({
        scrollTop: $(document).height()
    }, "fast");
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};