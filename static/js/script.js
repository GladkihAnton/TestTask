var task_id;
var task_status;
var dots = 1;
$(function () {
    var form_upload_file = $('#upload_file');
    var div_for_download = $('.for_download')
    form_upload_file.on('submit', function (e) {
        e.preventDefault();
        var form_data = new FormData($('#upload_file').get(0));
        var height = parseInt($('#id_height').val());
        var width = parseInt($('#id_width').val());
        if ((0<height && height<10000) && (0<width && width<10000)) {
            $.ajax({
                url: $(this).attr('action'),
                type: 'POST',
                data: form_data,
                cache: false,
                processData: false,
                contentType: false,
                success: function (data) {
                    task_id = data['task_id'];
                    task_status = data['task_status'];
                    setTimeout(check_result);
                    $('#id_file').prop('disabled', true);
                    $('#button_for_upload_file').prop('disabled', true);
                },
                error: function () {
                    console.log('error');
                }
            })
        }
        else {
            div_for_download.css('display', 'block');
            div_for_download.html('');
            div_for_download.append('Не верный формат чисел');
        }
    });
});
var check_result = function () {
    if (task_id) {
        var div_for_download = $('.for_download')
        var timer = setInterval(function () {
            var url = "/task/"+task_id;
            $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                task_status = data['task_status'];
                if (data['results']) {
                    div_for_download.css('display', 'block');
                    div_for_download.html('');
                    div_for_download.append('<a href="'+data['results']['archive_path']+'">download</a>');
                    clearInterval(timer);
                }
                else{
                    div_for_download.css('display', 'block');
                    if (dots == 4) {
                        div_for_download.html('');
                        dots = 1;
                    }
                    div_for_download.append('.');
                    dots += 1;
                }
            },
            error: function () {
                console.log('error');
            }
            })
        }, 800);
    }
};