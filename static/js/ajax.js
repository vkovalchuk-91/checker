function load(_url, _method, _data, success_func, before_func, complete_func) {
    $.ajax({
        url: _url,
        type: _method,
        data: _data,
        dataType: "json",
        headers:
            (_method.toUpperCase() !== 'GET')
                ? {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}
                : '',
        beforeSend: function () {
            before_func();
        },
        success: function (result) {
            success_func(result);
        },
        complete: function () {
            complete_func();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status >= 500) {
                notify_msg(textStatus, 'error');
            } else {
                notify_msg(jqXHR.responseText, 'error');
            }
        }
    });
}