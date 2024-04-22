document.addEventListener("DOMContentLoaded", () => {
    let logout_link = document.getElementById('logout-link');

    if (logout_link) {
        logout_link.addEventListener('click', function(e) {
            e.preventDefault()
            document.getElementById('logout-form').submit();
            }, false);
    }
});