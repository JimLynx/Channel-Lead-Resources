$(document).ready(function () {

    // clear flash messages after 5 seconds
    $(".alert").delay(5000).slideUp(1000);

    // set date format
    $("#date").datepicker({
        format: 'dd/mm/yyyy',
        startDate: '-3d'
    });
});
