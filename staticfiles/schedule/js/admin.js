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