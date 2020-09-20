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
});