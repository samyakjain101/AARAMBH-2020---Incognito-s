$(document).ready(function () {
    $('#post-form').on('submit', function (event) {
        event.preventDefault()
        $form = $(this)
        var formData = new FormData(this);
        $.ajax({
            type: "POST",
            url: window.location.pathname,
            data: formData,
            processData: false,
            contentType: false,
            success: handleFormSuccess,
        });
        function handleFormSuccess(data) {
            console.log('Success');
        }
    });

    $('.like').on('click', function (event) {
        event.preventDefault()
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