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

$( document ).ready(function() {
    var start = $("#id_start").val();
    var end = $("#id_end").val();
    var url = $("#export").data("check-sit-url");

    $.ajax({
        url: url,
        data: {
            'start': start,
            'end': end,
        },
        success: function(response) {
            if (response.length === 0) {
                $("#check").show();
            } else {
                 $("#warning").show().attr('data-bubble', JSON.stringify(response));

            }
        }
    });


$('#warning').hover(function(e) {

  // Get the value of the data-bubble attribute and parse it into a JavaScript array
  const bubbleList = $(this).data('bubble');

  // Create an empty bubble element
  const bubble = $('<div>').addClass('bubble');

  // Loop through the array and create a new <div> element for each item
  for (let i = 0; i < bubbleList.length; i++) {
    const bubbleItem = $('<div>').text(bubbleList[i]);
    // Append the bubbleItem to the bubble
    bubble.append(bubbleItem);
  }

  // Append the bubble to the document body
  $('body').append(bubble);

  // Position the bubble relative to the cursor
  const bubbleWidth = bubble.outerWidth();
  const bubbleHeight = bubble.outerHeight();
  const windowWidth = $(window).width();
  const windowHeight = $(window).height();
  const posX = e.pageX + 10;
  const posY = e.pageY + 10;

  if (posX + bubbleWidth > windowWidth) {
    bubble.css('left', e.pageX - bubbleWidth - 10);
  } else {
    bubble.css('left', posX);
  }

  if (posY + bubbleHeight > windowHeight) {
    bubble.css('top', e.pageY - bubbleHeight - 10);
  } else {
    bubble.css('top', posY);
  }

}, function() {
  // Remove the bubble when the mouse leaves the icon
  $('.bubble').remove();
});

});
