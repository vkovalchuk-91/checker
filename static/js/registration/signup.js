$(document).ready(function () {
    $(document)
        .on(
            'click', '.SignUpBtn', (evt) => {
                const target = evt.target;
                const form = $('#signUpForm');
                const data = getFormDataDict(form);
                // const data = form.serialize()
                // const contentType = 'application/json'
                load(
                    window.SignUpUrl,
                    'POST',
                    data,
                    (result) => {
                        window.location.href = "/accounts/login/";
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
