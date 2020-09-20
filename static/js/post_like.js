$(document).ready(function () {
    $('.like').on('click', function (event) {
        event.preventDefault()
        console.log('CLicked')
        var btn = $(this)
        $.ajax({
            type: "GET",
            url: btn.attr('url'),
            data: {
                'post_id': btn.attr('pid'),
            },
            success: handleFormSuccess,
        });
        function handleFormSuccess(json) {
            console.log(json.message);
        }
    });
});