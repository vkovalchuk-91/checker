$(document).ready(function () {
    $(document)
        .on(
            'click', '.SignUpBtn', (evt) => {
                const target = evt.target;
                const form = $('#signUpForm');
                const data = form.serialize()
                // const contentType = 'application/json'
                load(
                    window.SignUpUrl,
                    'POST',
                    data,
                    (result) => {
                        notify_msg("User registration successful", 'info')
                    },
                    () => {
                        target.disabled = true;
                    },
                    () => {
                        target.disabled = false;
                    },
                )
            }
        );
});
