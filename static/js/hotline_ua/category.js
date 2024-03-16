$(document).ready(function () {
    const $searchCategory = $('#search-category');
    const $searchCategoryResults = $('#search-category-results');

    $searchCategory.on('input', function () {
        $searchCategory.attr('data-value', null);
        const searchTerm = $(this).val().toLowerCase();

        if (searchTerm.length < 2) {
            $searchCategoryResults.html('');
            return
        }
        const data = {
            title: searchTerm,
            path: ''
        };

        load(
            window.CategoryUrl,
            'POST',
            data,
            (results) => {
                $searchCategoryResults.html('');
                if (results === undefined) {
                    return
                }

                results.forEach(result => {
                    const listItem = $('<li>').text(result.title);
                    listItem.val(result.path)

                    listItem.on('click', function () {
                        $searchCategory.val(result.title);
                        $searchCategory.attr('data-path', result.path);
                        $searchCategoryResults.hide();
                        update_filter();
                    });

                    $searchCategoryResults.append(listItem);
                });

                $searchCategoryResults.show()
            },
            () => {
                $searchCategory.disabled = true;
            },
            () => {
                $searchCategory.disabled = false;
            },
        )
    });

});