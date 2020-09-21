$(document).ready(function () {
    $('.post-card').on('click','.like' ,function (event) {
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
            if (json.likes_count){
                btn.closest('.card-body').find('.like-count').html(json.likes_count)
            }
        }
    });
    $('.post-card').on('submit', '#comment-form', function (event) {
        event.preventDefault()
        console.log('Comment')
        var form = $(this)
        form.find('button').html('<div class="spinner-grow spinner-grow-sm" role="status"> <span class="sr-only">Loading...</span> </div>');
        
        $.ajax({
            type: "POST",
            url: form.find('#comment-input').attr('url'),
            data: {
                'post_id': form.find('#comment-input').attr('pid'),
                'comment': form.find('#comment-input').val(),
                'csrfmiddlewaretoken': form.find("input[name=csrfmiddlewaretoken]").val()
            },
            success: handleFormSuccess,
        });

        function handleFormSuccess(json) {
            $.ajax({
                type: "GET",
                url: window.location.pathname,
                success: handleFormSuccess,
            });
            function handleFormSuccess(data) {
                var cardBody = $(data).find('.card-body').html();
                form.closest('.card-body').html(cardBody);
            }
        }
    });
});