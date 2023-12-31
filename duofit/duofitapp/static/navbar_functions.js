document.addEventListener('DOMContentLoaded', function () {
    var configBtn = document.getElementById('configButton');

    if (configBtn) {
        configBtn.addEventListener('click', function() {
            window.location.href = '/editconfig/';
        });
    }
});