function round(number, count) {
    return parseFloat(number).toFixed(parseInt(count));
}

function getFormDataDict(form) {
    const formDataArray = form.serializeArray();

    let formDataDict = {};
    formDataArray.forEach(function (entry) {
        formDataDict[entry.name] = entry.value;
    });

    return formDataDict;
}

function checker_count_update(count) {
    const $checkerCount = $("#checker-count");
    let new_count = parseInt($checkerCount.text());
    new_count += count;
    $checkerCount.text(new_count);

    const $allCount = $("#all-checker-count");
    if ($allCount.length > 0) {
        new_count = parseInt($allCount.text());
        new_count += count;
        $allCount.text(new_count);
    }
}
