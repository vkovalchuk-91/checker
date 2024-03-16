function update_filter() {
    const $selectBrand = $('#dselect-brand');
    const $selectShop = $('#dselect-shop');

    const $searchCategory = $('#search-category');
    const pathCategory = $searchCategory.attr('data-path');
    const titleCategory = $searchCategory.val();

    let data = {
        code: 0,
        title: '',
        category: {
            title: titleCategory.toLowerCase(),
            path: pathCategory,
        },
    };

    load(
        window.FilterUrl,
        'POST',
        data,
        (results) => {
            if ($.isArray(results) && results.length > 0) {
                $selectBrand.attr('multiple', 'multiple');
                $selectShop.attr('multiple', 'multiple');
                results.forEach(item => {
                    if (item.type_name.toLowerCase() === 'brand') {
                        $selectBrand.append('<option value="' + item.code + '">' + item.title + '</option>');
                    } else if (item.type_name.toLowerCase() === 'shop') {
                        $selectShop.append('<option value="' + item.code + '">' + item.title + '</option>');

                    }
                });
                dselect(document.querySelector('#dselect-brand'), config);
                dselect(document.querySelector('#dselect-shop'), config);
                $selectBrand.disabled = false;
                $selectShop.disabled = false;

                notify_toast('Filters updated.');
            }
        },
        () => {
            $selectBrand.val([]);
            $selectShop.val([]);
            $selectBrand.empty();
            $selectShop.empty();
            $selectBrand.removeAttr('multiple');
            $selectBrand.removeAttr('multiple');
            $selectBrand.disabled = true;
            $selectShop.disabled = true;
        },
        () => {
            // $selectBrand.disabled = false;
            // $selectShop.disabled = false;
        },
    )
}