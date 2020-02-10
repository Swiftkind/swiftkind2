$(document).ready(function() {
    //triggers navbar's menu to open or close

    var cameraPositionZ = 9000;
    $('.loading').addClass('site-loading');

    setTimeout(function() {
        cameraPositionZ = 30000;
        //hides the loading screen
        $('.loading').removeClass('site-loading');

        //displays the contents of the body after the loading screen
        $('body').addClass('site-loaded');

        //triggers the menu bar animation
        $('.menu-toggle').on('click', function() {
            $('body').toggleClass('menu-open');
        });

        // initialize swiper rtl
        var swiper = new Swiper('.swiper__generic', {


            pagination: {
                el: '.swiper-pagination',
                type: 'fraction',
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                1024: {
                    slidesPerView: 1,
                    spaceBetween: 55,
                },
                768: {
                    slidesPerView: 1,
                    spaceBetween: 0,
                },
                320: {
                    slidesPerView: 2,
                    spaceBetween: 0,
                    centeredSlides: true,
                }
            }
        });

        //testimony slider

        var swiper = new Swiper('.testimony--swiper', {
            pagination: {
                el: '.swiper-pagination'
            },
        });



        //initialize wow js

        wow = new WOW({
            boxClass: 'wow', // default
            animateClass: 'animated', // default
            offset: 0, // default
            mobile: true,
            live: true // default
        })
        wow.init();

        //initialize stickybits

        // $('.sticky').stickybits({
        //     useStickyClasses: true,
        //     stickyBitStickyOffset: 300
        // });


        //initialize rellax js

      var rellax = new Rellax('.rellax');

    }, 0);

    $.get('/blog/recent/', function( response ) {
        var template = $("#recent_blog_tpl").html();
        $("#recent_blog").html(_.template(template)({posts:response}));
    });
});