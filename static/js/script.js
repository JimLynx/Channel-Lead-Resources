$(document).ready(function () {

  // clear flash messages after 5 seconds
  $(".alert").delay(5000).slideUp(1000);

  // prevent whitespace for username and passwords inputs
  // Credit: adapted from https://stackoverflow.com/a/14236954
  $("input#username, input#password").on({
    keydown: function (e) {
      if (e.which === 32)
        return false;
    },
    change: function () {
      this.value = this.value.replace(/\s/g, "");
    }
  });

  // collapse resources if another clicked
  $('.resource-btn').click(function () {
    $('.collapse').collapse('hide');
  });

  // enable Bootstrap tooltips
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

  // stop videos playing when cancel button on modal clicked
  // Credit: https://stackoverflow.com/a/54845883
  $('.cancelVid').on('hidden.bs.modal', function (e) {
    let $iframes = $(e.target).find('iframe');
    $iframes.each(function (index, iframe) {
      $(iframe).attr('src', $(iframe).attr('src'));
    });
  });

});