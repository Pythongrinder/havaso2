$(document).ready(function() {
            var slider = $("#light-slider").lightSlider({
            item: 5 ,
            autoWidth: false,
            slideMove: 5, // slidemove will be 1 if loop is true
            slideMargin: 5,

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
            adaptiveHeight: true,

            vertical:false,
            verticalHeight:500,
            vThumbWidth:300,

            thumbItem:5,
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
                    item:5,
                    slideMove:5,
                  }
            },
            {
                breakpoint:480,
                settings: {
                    item:4,
                    slideMove:4,
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
        var decorator = $(this).children(".decorator").attr("value");
        var status = $(this).children(".status").attr("value");
        $('.jar-title').text(event.target.id)
        $('#decorator').text("Decorator: "+decorator)
        $('.description').text(alt)
        $('.jar-img-album').attr("src", src);
        $('#jarnumber').attr("value", id);

        if (status === "Available") {
        $('#jarnumber').prop("disabled", false);
        $('#jarnumber').text("Buy")
        $('#addwishlist').prop("disabled", false);

        } else {
            $('#jarnumber').prop("disabled", true);
            $('#jarnumber').text("SOLD")
            $('#addwishlist').prop("disabled", true);
        }

    });
});