$(document).ready(function () {
    console.log("loaded");
    $('#connection-request').on('click','button.confirm', function (event) {
        console.log("Clicked");
        var btn = $(this);
        event.preventDefault()

            $.ajax({
                type: "GET",
                url: btn.attr('url'),
                data: {
                    "sender": btn.attr('sender')
                },
                success: handleFormSuccess,
            });
            function handleFormSuccess(json) {
                console.log(json.message);
                console.log(json.error);
            } 
    });
});

