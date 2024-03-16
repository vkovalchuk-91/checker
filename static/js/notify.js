function notify_msg(message, messageType = 'error') {
    const $errors = $('#errorMessages');

    let items = '';
    if (messageType.toLowerCase() === 'error') {
        items += '<div class="alert alert-warning alert-dismissible fade show w-75" role="alert">';
    } else {
        items += '<div class="alert alert-info alert-dismissible fade show w-75" role="alert">';
    }
    items += '<strong>Exception:</strong> ';
    items += message;
    items += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
    items += '</div>';

    $errors.html(items);
    $errors.show();

}

function notify_toast(message) {
    $('#textToast').text(message);
    const toast = new bootstrap.Toast($('#infoToast'));
    toast.show();
}
