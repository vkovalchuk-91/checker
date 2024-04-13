function update_filter() {
    const $selectBase = $('#dselect-base');
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
                $selectBase.attr('multiple', 'multiple');
                $selectBrand.attr('multiple', 'multiple');
                $selectShop.attr('multiple', 'multiple');

                results.forEach(item => {
                    if (item.type_name.toLowerCase() === 'brand') {
                        $selectBrand.append('<option value="' + item.code + '">' + item.title + '</option>');
                    } else if (item.type_name.toLowerCase() === 'shop') {
                        $selectShop.append('<option value="' + item.code + '">' + item.title + '</option>');
                    } else if (item.type_name.toLowerCase() === 'link') {
                        $selectBase.append('<option value="' + item.code + '">' + item.title + '</option>');

                    }
                });

                dselect(document.querySelector('#dselect-base'), config);
                dselect(document.querySelector('#dselect-brand'), config);
                dselect(document.querySelector('#dselect-shop'), config);

                $selectBase.disabled = false;
                $selectBrand.disabled = false;
                $selectShop.disabled = false;

                notify_toast('Filters updated.');
            }
        },
        () => {
            $selectBase.val([]);
            $selectBrand.val([]);
            $selectShop.val([]);

            $selectBase.empty();
            $selectBrand.empty();
            $selectShop.empty();

            $selectBase.removeAttr('multiple');
            $selectBrand.removeAttr('multiple');
            $selectBrand.removeAttr('multiple');

            $selectBase.disabled = true;
            $selectBrand.disabled = true;
            $selectShop.disabled = true;
            $('#load-progressbar').removeAttr("hidden");
        },
        () => {
            // $selectBrand.disabled = false;
            // $selectShop.disabled = false;
            $('#load-progressbar').attr("hidden", "hidden");
        },
    )
}