$(document).ready(function () {
    $('#connection-request').on('click','button.confirm', function (event) {
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
    $('#connection-request').on('click','button.delete', function (event) {
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

