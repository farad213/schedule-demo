$( document ).ready(function() {

function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

     $('.icons > div').on('click', function(event) {
  if (isMobile()) {
    event.preventDefault();
  }
});


    $('.icons > div').hover(function() {
  if (this.classList.contains('true')) {
    // Get the value of the data-bubble attribute and parse it into a JavaScript array
    console.log($(this).data('bubble'))
    const bubbleList = JSON.parse($(this).data('bubble').replace(/'/g, '"'));

    // Create an empty bubble element
    const bubble = $('<div>').addClass('bubble');
    // Loop through the array and create a new <div> element for each item
    for (let i = 0; i < bubbleList.length; i++) {
      const bubbleItem = $('<div>').text(bubbleList[i]);
      // Append the bubbleItem to the bubble
      bubble.append(bubbleItem);
    }
    // Append the bubble to the icon
    $(this).append(bubble);
  }
}, function() {
  // Remove the bubble when the mouse leaves the icon
  $(this).find('.bubble').remove();


});
  var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!

today = mm + '/' + dd;

$('.day .date').each(function() {
    console.log(today, $(this).text())
    if ($(this).text() === today) {
        $(this).closest('.day').attr('id', 'today');
    }
});

 $(".toggle-days-displayed input[name='toggle-days-displayed']").click(function() {
        if ($(this).val() === "5 nap") {
            $(".weekend, .Szombat-display, .Vasárnap-display").css("display", "none");
            $(".day_wrap, .weekdays div").css("margin", "10px 20px 10px 20px");
        } else {
            $(".weekend, .Szombat-display, .Vasárnap-display").css("display", "block");
            $(".day_wrap, .weekdays div").css("margin", "10px");
        }
    });

});

//$( document ).ready(function() {
//    $("#export").click(function() {
//        var start = $("#id_start").val();
//        var end = $("#id_end").val();
//        var url = $(this).data("export-url")
//
//
//        $.ajax({
//    url: url,
//    data: {
//        'start': start,
//        'end': end,
//    },
//    success: function(response) {
//        var blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
//        var link = document.createElement('a');
//        link.href = window.URL.createObjectURL(blob);
//        link.download = "my_file.xlsx";
//        link.click();
//    }
//});
//    });
//});
