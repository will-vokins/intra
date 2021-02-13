function loadLoader() {
    document.getElementById('loaderContainer').style.cssText = 'display: block;';
}

function mobileMenu() {
    var x = document.getElementById("mobileNav");
    if (x.style.display === "block") {
        x.style.display = "none";
    } else {
        x.style.display = "block";
    }
}

$(document).ready(function() {

    $('.submit_on_enter').keydown(function(event) {
        // enter has keyCode = 13, change it if you want to use another button
        if (event.keyCode == 13) {
            this.form.submit();
            return false;
        }
    });

});