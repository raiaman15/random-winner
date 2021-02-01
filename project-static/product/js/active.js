(function ($) {
    'use strict';

    var browserWindow = $(window);

    // :: 1.0 Preloader Active Code
    browserWindow.on('load', function () {
        $('#preloader').fadeOut('slow', function () {
            $(this).remove();
        });
    });

    // :: 2.0 Nav Active Code
    if ($.fn.classyNav) {
        $('#cryptosNav').classyNav();
    }

    // :: 3.0 Sliders Active Code
   

    // :: 4.0 Gallery Active Code
    if ($.fn.magnificPopup) {
        $('.videobtn').magnificPopup({
            type: 'iframe'
        });
    }

    // :: 5.0 ScrollUp Active Code
    if ($.fn.scrollUp) {
        browserWindow.scrollUp({
            scrollSpeed: 1500,
            scrollText: '<i class="fa fa-angle-up"></i>'
        });
    }

    // :: 6.0 CouterUp Active Code
    if ($.fn.counterUp) {
        $('.counter').counterUp({
            delay: 10,
            time: 2000
        });
    }

    // :: 7.0 wow Active Code
    if (browserWindow.width() > 767) {
        new WOW().init();
    }
    
    // :: 8.0 prevent default a click
    $('a[href="#"]').click(function ($) {
        $.preventDefault()
    });

})(jQuery);

 // year 
      var date = new Date().getFullYear();
$(".year").append(date);
    

var $owl = $('#carousel1');
$owl.children().each(function (index) {
    $(this).attr('data-position', index);

});
$('#carousel1').owlCarousel({
    loop: true,
    center: true,
    margin: 0,
    responsiveClass: true,
    nav: false,
    autoplay: true,
    autoplayTimeout: 5000,
    autoplayHoverPause: true,

    responsive: {
        0: {
            items: 1
        },
        680: {
            items: 2
        },
        1000: {
            items: 3
        }
    }
})
$(document).on('click', '.owl-item>div', function () {
    var $speed = 1000;
    $owl.trigger('to.owl.carousel', [$(this).data('position'), $speed]);
});