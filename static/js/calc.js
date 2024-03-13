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

$(document).ready(function() {
  var currentPageUrl = window.location.href;

  $('.nav-link').each(function() {
    var menuItemUrl = $(this).attr('href');
    if (currentPageUrl.includes(menuItemUrl)) {
      $(this).addClass('text-primary-emphasis active');
    } else {
        $(this).removeClass('text-primary-emphasis')
    }
  });
});