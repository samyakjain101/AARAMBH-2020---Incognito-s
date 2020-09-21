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
        var form = $(this)
        console.log(form.find("input[name=csrfmiddlewaretoken]"));
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
            console.log(json.message);
        }
    });
});