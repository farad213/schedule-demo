$('.icons > div').hover(function() {
  if (this.classList.contains('true')) {
    const bubble = $('<div>').addClass('bubble').text(this.classList[0]);
    $(this).append(bubble);
  }
}, function() {
  $(this).find('.bubble').remove();
});