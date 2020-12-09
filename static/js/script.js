$(document).ready(function () {

    // clear flash messages after 5 seconds
    $(".alert").delay(5000).slideUp(1000);

    // stop videos playing when cancel button on modal clicked
    $('.cancelVid').click(function () {
        $('iframe').attr('src', $('iframe').attr('src'));
    });
});
