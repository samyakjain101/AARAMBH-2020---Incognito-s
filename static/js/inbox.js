$(document).ready(function () {
    console.log("loaded");
    $('.new_chat_btn').on('click', function (event) {
        console.log("Clicked");
        var btn = $(this);
        event.preventDefault()

        $.ajax({
            type: "GET",
            url: btn.attr('url'),
            data: {
                "user_id": btn.attr('user_id')
            },
            success: handleFormSuccess,
        });
        function handleFormSuccess(json) {
            console.log(json.message);
            if(json.redirect){
                window.location.href = '/chat/message/' + json.redirect;
            }
        }
    });
});

