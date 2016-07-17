$(function() {
    setInterval(function(){
        $(".success").fadeOut("slow");
    }, 2000);


    $('.ratingjs2').html('<span class="stars">'+parseFloat($('.ratingjs').html())+'</span>');
    $('span.stars').stars();

});
// Rating system
$.fn.stars = function() {
    return $(this).each(function() {
        $(this).html($('<span />').width(Math.max(0, (Math.min(5, parseFloat($(this).html())))) * 16));
    });
}
