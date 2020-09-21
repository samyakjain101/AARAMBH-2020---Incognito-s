$(document).ready(function () {
    $('.blog_area').on('submit', '#comment-form', function (event) {
        event.preventDefault()
        console.log('Comment')
        var form = $(this)
        form.find('button').html('<div class="spinner-grow spinner-grow-sm" role="status"> <span class="sr-only">Loading...</span> </div>');
        $.ajax({
            type: "POST",
            url: form.find('#comment-input').attr('url'),
            data: {
                'blog_id': form.find('#comment-input').attr('pid'),
                'comment': form.find('#comment-input').val(),
                'csrfmiddlewaretoken': form.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: handleFormSuccess,
        });
        function handleFormSuccess(json) {
            console.log(json.message);
            $.ajax({
                type: "GET",
                url: window.location.pathname,
                success: handleFormSuccess, 
            });
            function handleFormSuccess(data) {
                var commentBody = $(data).find('.comments-area').html();
                form.closest('.comments-area').html(commentBody);
            }
        }
    });
});