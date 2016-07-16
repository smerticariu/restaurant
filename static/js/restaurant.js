$(function() {
    setInterval(function(){
        $(".success").fadeOut("slow");
    }, 2000);


        $('.ratingjs2').html('<span class="stars">'+parseFloat($('.ratingjs').html())+'</span>');
        $('span.stars').stars();

            // $('input[type=submit]').click();

$('.ratingjs2__client').html('<span class="stars">'+parseFloat($('.ratingjs__client').html())+'</span>');
        //$('span.stars').stars();

        });
$.fn.stars = function() {
    return $(this).each(function() {
        $(this).html($('<span />').width(Math.max(0, (Math.min(5, parseFloat($(this).html())))) * 16));
    });
}
