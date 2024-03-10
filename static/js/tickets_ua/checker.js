$(document).ready(function () {
    $('#range-time').on('input', function () {
        const time = $('#range-time').val()
        $('#range-time-value').val((time < 10 ? "0" + time : time) + ":00")
    });

    $(document)
        .on(
            'click', '.CreateCheckerBtn', (evt) => {
                const target = evt.target;
                const form = $('#createCheckerForm');
                let data = getFormDataDict(form)

                const to_station_value = $('#search-to')[0].dataset.value;
                if (to_station_value) {
                    data.to_station = to_station_value;
                }

                const from_value_value = $('#search-from')[0].dataset.value;
                if (from_value_value) {
                    data.from_station = from_value_value;
                }

                load(
                    window.ChekerUrl,
                    'POST',
                    data,
                    (result) => {
                        const table = $('#checkersBodyTable');
                        $.each(result, function (i, item) {
                            const dateParts = item.date_at.split(' ');
                            const timeParts = item.time_at.split(':');
                            table.append(
                                '<tr>' +
                                '   <td>' + item.from_station.name + '</td>' +
                                '   <td>' + item.to_station.name + '</td>' +
                                '   <td>' + dateParts[0] + '</td>' +
                                '   <td>' + timeParts[0] + ':' + timeParts[1] + '</td>' +
                                '   <td>' +
                                '       <div class="form-check d-flex justify-content-center">' +
                                '           <input class="form-check-input activeCheckerButton" type="checkbox"' +
                                '               value="' + item.is_active + '" aria-label="checker_active_state" ' +
                                '               data-checker_id="' + item.id + '" checked >' +
                                '       </div>' +
                                '   </td>' +
                                '   <td></td>' +
                                '   <td>' +
                                '       <div class="input-group d-flex justify-content-center">' +
                                '           <button title="trash" class="nav-link bi bi-trash mx-1 deleteCheckerButton"' +
                                '                   data-checker_id="' + item.id + '"' +
                                '       </div>' +
                                '   </td>' +

                                '</tr>'
                            );
                        });
                        notify_msg("Checkers save successful", 'info')
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
    $(document)
        .on(
            'click', '.deleteCheckerButton', (evt) => {
                const target = evt.target;
                const checker_id = target.dataset.checker_id;
                // const data = {
                //     'id': checker_id,
                // };
                load(
                    window.ChekerUrl + checker_id + '/',
                    'DELETE',
                    null,
                    () => {
                        $('#checkersBodyTable').find('button[data-checker_id="' + checker_id + '"]').closest('tr').remove();
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
    $(document)
        .on(
            'click', '.activeCheckerButton', (evt) => {
                const target = evt.target;
                const checker_id = target.dataset.checker_id;

                const data = {
                    'is_active': $(evt.target).prop('checked'),
                };
                load(
                    window.ChekerUrl + checker_id + '/',
                    'PUT',
                    data,
                    (result) => {
                        $(evt.target).prop('checked', result.is_active);
                    },
                    () => {
                        target.disabled = true;
                    },
                    () => {
                        setTimeout(function () {
                            target.disabled = false;
                        }, 2000);
                    },
                )
            }
        );
});