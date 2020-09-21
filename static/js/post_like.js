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
    $('#comment-form').on('submit', function (event) {
        event.preventDefault()
        console.log('Comment')
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
});