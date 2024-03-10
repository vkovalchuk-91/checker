$(document).ready(function () {
    const $searchFrom = $('#search-from');
    const $searchFromResults = $('#search-from-results');


    const $searchTo = $('#search-to');
    const $searchToResults = $('#search-to-results');

    $searchFrom.on('input', function () {
        $searchFrom.attr('data-value', null);
        const searchTerm = $(this).val().toLowerCase();


        if (searchTerm.length < 2) {
            $searchFromResults.html('');
            return
        }
        const data = {
            name: searchTerm,
            code: 0
        };

        load(
            window.StationUrl,
            'POST',
            data,
            (results) => {
                $searchFromResults.html('');
                if (results === undefined) {
                    return
                }

                results.forEach(result => {
                    const listItem = $('<li>').text(result.name);
                    listItem.val(result.code)

                    listItem.on('click', function () {
                        $searchFrom.val(result.name);
                        $searchFrom.attr('data-value', result.code);
                        $searchFromResults.hide();
                    });

                    $searchFromResults.append(listItem);
                });

                $searchFromResults.show();
            },
            () => {
                $searchFrom.disabled = true;
            },
            () => {
                $searchFrom.disabled = false;
            },
        )
    });

    $searchTo.on('input', function () {
        $searchTo.attr('data-value', null);
        const searchTerm = $(this).val().toLowerCase();


        if (searchTerm.length < 2) {
            $searchToResults.html('');
            return
        }
        const data = {
            'name': searchTerm,
            'code': 0
        };

        load(
            window.StationUrl,
            'POST',
            data,
            (results) => {
                $searchToResults.html('');
                if (results === undefined) {
                    return
                }

                results.forEach(result => {
                    const listItem = $('<li>').text(result.name);
                    listItem.val(result.code)

                    listItem.on('click', function () {
                        $searchTo.val(result.name);
                        $searchTo.attr('data-value', result.code);
                        $searchToResults.hide();
                    });

                    $searchToResults.append(listItem);
                });

                $searchToResults.show();
            },
            () => {
                $searchTo.disabled = true;
            },
            () => {
                $searchTo.disabled = false;
            },
        )
    });
});