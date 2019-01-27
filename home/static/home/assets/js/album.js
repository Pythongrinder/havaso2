$(document).ready(function() {
            var slider = $("#light-slider").lightSlider({
            item: 8,
            autoWidth: false,
            slideMove: 8, // slidemove will be 1 if loop is true
            slideMargin: 10,

            addClass: '',
            mode: "slide",
            useCSS: true,
            cssEasing: 'ease', //'cubic-bezier(0.25, 0, 0.25, 1)',//
            easing: 'linear', //'for jquery animation',////

            speed: 400, //ms'
            auto: false,
            pauseOnHover: false,
            loop: false,
            slideEndAnimation: true,
            pause: 2000,

            keyPress: false,
            controls: false,
            prevHtml: '',
            nextHtml: '',

            rtl:false,
            adaptiveHeight:false,

            vertical:false,
            verticalHeight:500,
            vThumbWidth:100,

            thumbItem:10,
            pager: true,
            gallery: false,
            galleryMargin: 5,
            thumbMargin: 1,
            currentPagerPosition: 'middle',

            enableTouch:true,
            enableDrag:false,
            freeMove:true,
            swipeThreshold: 40,

            responsive : [
            {
                breakpoint:800,
                settings: {
                    item:6,
                    slideMove:6,
                  }
            },
            {
                breakpoint:480,
                settings: {
                    item:5,
                    slideMove:5,
                  }
            }
        ],

            onBeforeStart: function (el) {},
            onSliderLoad: function (el) {},
            onBeforeSlide: function (el) {},
            onAfterSlide: function (el) {},
            onBeforeNextSlide: function (el) {},
            onBeforePrevSlide: function (el) {}
        });

$('#goToPrevSlide').on('click', function () {
    slider.goToPrevSlide();
});
$('#goToNextSlide').on('click', function () {
    slider.goToNextSlide();
});


    });



    $(document).ready(function() {
    $(".getid").click(function(event) {
        var alt = $(this).children("img").attr("alt");
        var src = $(this).children("img").attr("src");
        var id = $(this).children("input").attr("value");
        $('.jar-title').text(event.target.id)
        $('.description').text(alt)
        $('.jar-img-album').attr("src", src);
        $('#jarnumber').attr("value", id);


    });
});

// this is the id of the form
$("#addwishlist").click(function() {

    var url = '/wishlist/add/';
    var jarnumber = $('#jarnumber').attr("value");
    var data = {jar: jarnumber}

    $.ajax({
           type: "POST",
           url: url,
           data: data,
           success: function(data)
           {

              console.log(data)

           }
         });


});


// this is the id of the form
$("#buyjar").click(function() {

    var url = '/wishlist/add/';
    var jarnumber = $('#jarnumber').attr("value");
    var data = {jar: jarnumber}

    $.ajax({
           type: "POST",
           url: url,
           data: data,
           success: function(data)
           {

              window.location.href = "/shop/"

           }
         });


});
