  google.load("visualization", "1", {packages:["corechart"]});

  // Reload page
  function reload() {
      location.reload(true);
  }

  // Show hide code bubbles
  function toggle(id) {
    $('.code-example').not(id).hide();
    $(id).toggle();
  }

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
  function delete_service(name, key) {
      $.ajax({
          type: "POST",
          url: "/delete",
          data: {"name": name, "api_key": key},
          success: function () {
              var text = 'Alert has been deleted. Refresh to see update. ' + name;
              $("#alert").text(text).slideDown(2000).delay(2000).slideUp(2000);
          }
      });
      return false;
  }

  // Get historical data
  function getHistoricalData(name) {
      var url = '/api/?' + $.param({'name': name, 'api_key': PUBLIC_KEY});

      return $.parseJSON($.ajax({
          type: "GET",
          url: url,
          async: false
      }).responseText);

  }

  // Transform historical data
  function transformHistoricalData(historicalData) {

      for (var i = 0; i < historicalData.length; i++) {
          historicalData[i][0] = new Date(historicalData[i][0]);
      }
      historicalData.unshift(['Time', 'Actual Value']);
      return historicalData;
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
