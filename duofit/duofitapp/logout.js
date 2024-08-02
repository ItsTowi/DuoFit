// script.js
document.addEventListener('DOMContentLoaded', function () {
    var logoutButton = document.getElementById('logoutButton');

    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            window.location.href = '/logout/';
        });
    }
});
