function notify_msg(message, messageType = 'error') {
    const $errors = $('#errorMessages');

    let items = '';
    if (messageType.toLowerCase() === 'error') {
        items += '<div class="alert alert-warning alert-dismissible fade show" role="alert">';
    } else {
        items += '<div class="alert alert-info alert-dismissible fade show" role="alert">';
    }
    items += '<strong>Exception:</strong> ';
    items += message;
    items += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    items += '</div>';

    $errors.html(items);
    $errors.show();

}