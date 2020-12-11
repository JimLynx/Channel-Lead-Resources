$(document).ready(function () {

    // clear flash messages after 5 seconds
    $(".alert").delay(5000).slideUp(1000);

    // stop videos playing when cancel button on modal clicked
    $('.cancelVid').click(function () {
        $('iframe').attr('src', $('iframe').attr('src'));
    });

    // prevent whitespace for username and passwords inputs
    // Credit: adapted from https://stackoverflow.com/a/14236954
    $("input#username, input#password").on({
        keydown: function(e) {
          if (e.which === 32)
            return false;
        },
        change: function() {
          this.value = this.value.replace(/\s/g, "");
        }
      });
});
