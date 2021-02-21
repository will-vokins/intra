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
        if (event.keyCode == 13) {
            this.form.submit();
            return false;
        }
    });

});


$(document).ready(function() {
    $("#inviteLink").click(function() {
        $("#inviteBox").animate({
            height: "40px"
        }, 200, function() {

        });
    });
});

$(function() {
    $('#newClientSubmit').click(function() {
        $('#newClientSubmit').hide();
        $('#workerButton').show();
        $.ajax({
            url: '/clients/new',
            data: $('#newClientForm').serialize(),
            type: 'POST',
            success: function(jqXHR, response) {
                $('#flash').html("Invitation sent!");
                $('#flash').addClass("flash--visible flash--success");
                $('#flash').removeClass("flash--error");
                $("#workerButton").html("&#10004;");
                setTimeout(function() {

                    $("#workerButton").html("<div class=\"myloader\">Loading...</div>");
                    $('#newClientSubmit').show();
                    $('#workerButton').hide();
                    $('#flash').removeClass("flash--visible")
                    $("#inviteBox").animate({
                        height: "0px"
                    }, 200, function() {});

                }, 2000);
            },
            error: function(jqXHR, error) {
                if (jqXHR.status === 400) {
                    $('#flash').html("Client already has a pending invitation.");
                }
                if (jqXHR.status === 590) {
                    $('#flash').html("Please enter a valid email address.");
                }
                if (jqXHR.status === 401) {
                    $('#flash').html("Unauthorized - are you logged in?");
                }
                $('#flash').addClass("flash--visible flash--error");
                $('#flash').removeClass("flash--success");
                $("#workerButton").html("&#10006;");
                setTimeout(function() {

                    $("#workerButton").html("<div class=\"myloader\">Loading...</div>");
                    $('#newClientSubmit').show();
                    $('#workerButton').hide();
                    $('#flash').removeClass("flash--visible")

                }, 2500);
            }
        });
        return false
    });
});