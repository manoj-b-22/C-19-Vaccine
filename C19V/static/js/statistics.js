// Code for Bar Graph's Bar Animation
$(function(){
    $('.bars li .bar').each(function(key, bar){
        var percentage = $(this).data('percentage');
        $(this).animate({
            'height':percentage + '%'
        },1000);
    });
});