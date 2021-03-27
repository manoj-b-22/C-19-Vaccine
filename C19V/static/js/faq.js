$(document).ready(function() {
    $(".faqs-container .faq-singular:first-child").addClass("active").children(".faq-answer").slideDown();
    $(".faq-question").on("click", function() {
        if ($(this).parent().hasClass("active")) {
            $(this).next().slideUp();
            $(this).parent().removeClass("active");
        } else {
            $(".faq-answer").slideUp();
            $(".faq-singular").removeClass("active");
            $(this).parent().addClass("active");
            $(this).next().slideDown();
        }
    });
});