  google.load("visualization", "1", {packages:["corechart"]});

  // Show hide code bubbles
  function toggle(id) {
    $('.code-example').not(id).hide();
    $(id).toggle();
  };

  // Submit form without redirect
  $(function () {
    $('#example-form').submit(function () {
        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: $(this).serialize(),
            success: location.reload(true)
          });
        return false;
    });
  });

  // Delete service by name
  function delete_service(name) {
      $.ajax({
          type: "POST",
          url: "http://www.clowder.io/delete",
          data: {"name": name, "api_key": "{{ user.company.public_key }}"},
          success: location.reload(true)
      });
      return false;
  }

  // Let users show/hide charts
  $(document).ready(function() {
    $(".service-item").click(function() {
        $(this).find(".service-item-chart").toggle();
    });

    $(".show-all-services").click(function() {
        $(".service").show();
    });

    $(".show-passing-services").click(function() {
        $(".service-passing").show();
        $(".service-failing").hide();
    });

    $(".show-failing-services").click(function() {
        $(".service-passing").hide();
        $(".service-failing").show();
    });
  });
