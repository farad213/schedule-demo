$( document ).ready(function() {
 $(".toggle-days-displayed input[name='toggle-days-displayed']").click(function() {
        if ($(this).val() === "5 nap") {
            $(".weekend, .Szombat-display, .Vasárnap-display").css("display", "none");
            $(".day_wrap, .weekdays div").css("margin", "10px 20px 10px 20px");
        } else {
            $(".weekend, .Szombat-display, .Vasárnap-display").css("display", "block");
            $(".day_wrap, .weekdays div").css("margin", "10px");
        }
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

$(".disabled_a").on("click", function(event) {
  event.preventDefault();
});

});
