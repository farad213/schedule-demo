$(document).ready(function() {
    $('#calculate').click(function(e) {
      e.preventDefault(); // prevent the form from submitting normally
      var radioValue = $("input[type='radio']:checked").val();
      var sorszam = $("#sorszam").val();
      var url = $("#box").data("url");
      $.ajax({
        url: url, // replace with the appropriate endpoint
        type: 'GET', // or POST, depending on your requirements
        data: {"sorszam": sorszam, "building": radioValue},
        success: function(data) {
          $('#result').text(data); // update the text in the #result element with the response from the server
          $("#sorszam").val("");
        }
      });
    });
  });