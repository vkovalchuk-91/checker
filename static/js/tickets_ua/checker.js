$(document).ready(function () {
    $(document)
        .on(
            'click', '.CreateCheckerBtn', (evt) => {
                const target = evt.target;
                const form = $('#createCheckerForm');
                let data = getFormDataDict(form)

                const from_value_value = $('#search-from')[0].dataset.value;
                data.from_station = {name: data.from_station, code: from_value_value}

                const to_station_value = $('#search-to')[0].dataset.value;
                data.to_station = {name: data.to_station, code: to_station_value}

                load(
                    window.ChekerUrl,
                    'POST',
                    data,
                    (result) => {
                        const table = $('#checkersBodyTable');
                        $.each(result, function (i, item) {
                            const dateParts = item.date_at.split(' ');
                            const timeParts = item.time_at.split(':');
                            const newRow = '<tr>' +
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

                                '</tr>';
                            table.append(newRow);
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