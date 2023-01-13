$(document).ready(function() {
    $('#calculate').click(function(e) {
      e.preventDefault(); // prevent the form from submitting normally
      var ccs = $("#ccs").val();
      var vvs = $("#vvs").val();
      var url = $("#box").data("url");
      $.ajax({
        url: url, // replace with the appropriate endpoint
        type: 'GET', // or POST, depending on your requirements
        data: {"ccs": ccs, "vvs": vvs},
        success: function(data) {
          $('#result').text(data); // update the text in the #result element with the response from the server
          $("#ccs").val("");
          $("#vvs").val("");
        }
      });
    });
  });