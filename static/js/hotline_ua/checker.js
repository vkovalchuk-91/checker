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
                $('#dselect-shop option:selected').each(function () {
                    selectedFilters.push({
                        title: $(this).text(),
                        code: $(this).val(),
                        category: category,
                    });
                });

                $('#dselect-brand option:selected').each(function () {
                    selectedFilters.push({
                        title: $(this).text(),
                        code: $(this).val(),
                        category: category,
                    });
                });

                const search_text = $('#search-text').val()
                if (search_text !== null && search_text !== undefined && search_text !== '') {
                    selectedFilters.push({
                        title: search_text,
                        type_name: 'text',
                        category: category,
                    });
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
                                    item_filters += item_filter.title + '-';
                                });

                            table.append(
                                '<tr>' +
                                '   <td><small>' + (item.category === null ? '' : item.category.title) + '</small></td>' +
                                '   <td><small>' + item_filters + '</small></td>' +
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


// $(document).ready(function () {
//     const $searchCategory = $('#search-category');
//     const $searchCategoryResults = $('#search-category-results');
//
//
//     $searchCategory.on('input', function () {
//         $searchCategory.attr('data-value', null);
//         const searchTerm = $(this).val().toLowerCase();
//
//         var selectedOptions = $('#dselect-brand').val();
//         JSON.stringify({ selectedOptions: selectedOptions })
//
//         if (searchTerm.length < 2) {
//             $searchCategoryResults.html('');
//             return
//         }
//         const data = {
//             title: searchTerm,
//             path: ''
//         };
//
//         load(
//             window.CategoryUrl,
//             'POST',
//             data,
//             (results) => {
//                 $searchCategoryResults.html('');
//                 if (results === undefined) {
//                     return
//                 }
//
//                 results.forEach(result => {
//                     const listItem = $('<li>').text(result.title);
//                     listItem.val(result.path)
//
//                     listItem.on('click', function () {
//                         $searchCategory.val(result.title);
//                         $searchCategory.attr('data-path', result.path);
//                         $searchCategoryResults.hide();
//                         update_filter();
//                     });
//
//                     $searchCategoryResults.append(listItem);
//                 });
//
//                 $searchCategoryResults.show();
//             },
//             () => {
//                 $searchCategory.disabled = true;
//             },
//             () => {
//                 $searchCategory.disabled = false;
//             },
//         )
//     });
//
// });