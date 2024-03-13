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
