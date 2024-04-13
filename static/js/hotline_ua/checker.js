$(document).ready(function () {
    $(document)
        .on(
            'click', '.CreateCheckerBtn', (evt) => {
                const target = evt.target;

                const $searchCategory = $('#search-category');
                const category = {
                    title: $searchCategory.val(),
                    path: $searchCategory.attr('data-path'),
                };

                let selectedFilters = [];
                $('#dselect-base option:selected').each(function () {
                    const titleContent = $(this).text();
                    const codeContent = $(this).val();
                    let selectedFilter = {
                        title: titleContent,
                        category: category,
                        type_name: 'link',
                    };
                    if (Number.isInteger(parseInt(codeContent))) {
                        selectedFilter.code = parseInt(codeContent);
                    }
                    selectedFilters.push(selectedFilter);
                });


                $('#dselect-shop option:selected').each(function () {
                    const titleContent = $(this).text();
                    const codeContent = $(this).val();
                    let selectedFilter = {title: titleContent, category: category, type_name: 'shop',};
                    if (Number.isInteger(parseInt(codeContent))) {
                        selectedFilter.code = parseInt(codeContent);
                    }
                    selectedFilters.push(selectedFilter);
                });

                $('#dselect-brand option:selected').each(function () {
                    const titleContent = $(this).text();
                    const codeContent = $(this).val();
                    let selectedFilter = {title: titleContent, category: category, type_name: 'brand',};
                    if (Number.isInteger(parseInt(codeContent))) {
                        selectedFilter.code = parseInt(codeContent);
                    }
                    selectedFilters.push(selectedFilter);
                });

                const search_text = $('#search-text').val()
                if (search_text !== null && search_text !== undefined && search_text !== '') {
                    selectedFilters.push({
                        title: search_text,
                        type_name: 'text',
                        category: category,
                    });
                }

                const priceRange = priceSlider.getValue()
                const priceArray = $.map(priceRange.split(','), function (num) {
                    return parseInt(num, 10);
                });
                if (category.title.length > 0 && priceArray[0] <= priceArray[1]) {
                    if (priceArray[0] > 0) {
                        selectedFilters.push({
                            code: priceArray[0],
                            title: 'min',
                            type_name: 'min',
                            category: category,
                        });
                    }
                    if (priceArray[1] < maxRange) {
                        selectedFilters.push({
                            code: priceArray[1],
                            title: 'max',
                            type_name: 'max',
                            category: category,
                        });
                    }
                }

                const data = {
                    category: category,
                    filters: selectedFilters,
                }

                load(
                    window.ChekerUrl,
                    'POST',
                    data,
                    (result) => {
                        const table = $('#checkersBodyTable');
                        $.each(result, function (i, item) {
                            let item_filters = '';
                            if (item.filters !== null)
                                item.filters.forEach(item_filter => {
                                    item_filters += '' +
                                        '   <small title="' + item_filter.type_name + '">' +
                                        '       ' + item_filter.title + ',' +
                                        '   </small>';
                                });

                            table.append(
                                '<tr>' +
                                '   <td><small>' + (item.category === null ? '' : item.category.title) + '</small></td>' +
                                '   <td>' + item_filters + '</td>' +
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
                        checker_count_update(result.length);
                        notify_msg("Checkers save successful", 'info');
                    },
                    () => {
                        target.disabled = true;
                        $('#load-progressbar').removeAttr("hidden");
                    },
                    () => {
                        target.disabled = false;
                        $('#load-progressbar').attr("hidden", "hidden");
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
                        checker_count_update(-1);
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
