// display Searching Progress Bar
function displaySearchingProgress() {
    let html = `
            <div class="progress" role="progressbar" aria-label="Animated striped example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
              <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
            </div>`
    $('#main_content').html(html);
}