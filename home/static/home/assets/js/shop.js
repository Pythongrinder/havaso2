$(document).on("click", "#tocheckout", function() {

    var singleData = $("textarea:eq(1)").val();

    var url = '/shop/getcheckout/';

    if (singleData) {
        var data = {
            puprosetext: singleData
        }
    } else {
        singleData = $('#shopselector option:selected').val();
        var data = {
            puprosetext: singleData
        }

    }



    $.ajax({
        type: "GET",
        url: url,
        data: data,
        success: function(data) {

            window.location.href = '/shop/payment/'

        }
    });

});


//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
$(".next").click(function() {
    var current_fs = $(this).parent();
    var next_fs = $(this).parent().next();
    var purpose = $('#purpose option:selected').val();

    if (purpose === 'Choose an option') {
        // DOES NOT DO ANYTHING
    } else if (purpose === 'Personal') {
        console.log(purpose)
        animating = true;
        next_fs.show();
        $("#shopselector").hide();
        $('#shoppage2').prepend('<div class="boxtitle"><h2 class="fs-title">Step 2 - General Jar</h2>' +
            '<p>You have chosen a General Jar.</p> <p> Price: € 42,50</p> <p>Describe the purpose for your jar.</p>' +
            '<textarea id="textInput" rows="4" cols="50"> </textarea>' +
            '<small class="text-muted">Please give a short description of your goal or objective. May be keywords.</small></div>')

        var url = '/shop/getcheckout/';
        var data = {
            purpose: purpose
        }
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function(data) {}
        });

        /// WORKING

    } else if (purpose === 'General') {
        $('#shoppage2').prepend('<div class="boxtitle"><h2 class="fs-title">Step 2 - Personal Jar</h2>' +
            '<p>You have chosen a Personal Jar.</p> <p> Price: €27.50 </p> <p>Find your purpose</p></div>')
        animating = true;
        var url = '/shop/getcheckout/';
        var data = {
            purpose: purpose
        }

        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function(data) {
                $("#shopselector option").each(function() {
                    $(this).remove();
                });
                $('#addq').find(':first-child').remove();

                if (typeof data !== 'string') {
                    jQuery.each(data, function(i, val) {
                        jQuery.each(val, function(i, val) {
                            next_fs.show();
                            $('#shopselector').prepend("<option class='opval' value='" + val['keyword'] + "'>" + val['keyword'] + "</option>");
                        });
                    });
                }
            }
        });
        next_fs.show();


        /// NOT WORKING YET
    } else {
        animating = true;
        $("#shopselector").hide();
        next_fs.show();
        $('#shoppage2').prepend('<div class="boxtitle"><h2 class="fs-title">Step 2 - Guided Jar</h2>' +
            '<p>You have chosen a Guided Jar.</p> <p> Price: € 75,00</p> ' +
            '<p>After payment you will be directed to an appointment picker. Make an appointment to finish your order.</p>' +
            '<textarea class="describe" rows="4" cols="50"> </textarea>' +
            '<small class="text-muted">Please provide us with your ideas, thoughts or doubts to have a starting point for our call. May be keywords</small></div>')

        var url = '/shop/getcheckout/';
        var data = {
            purpose: purpose
        }
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            success: function(data) {}
        });



    }


    if (animating) {
        //activate next step on progressbar using the index of next_fs
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
        //show the next fieldset
        //hide the current fieldset with style
        current_fs.animate({
            opacity: 0
        }, {
            step: function(now, mx) {
                //as the opacity of current_fs reduces to 0 - stored in "now"
                //1. scale current_fs down to 80%
                scale = 1 - (1 - now) * 0.2;
                //2. bring next_fs from the right(50%)
                left = (now * 50) + "%";
                //3. increase opacity of next_fs to 1 as it moves in
                opacity = 1 - now;
                current_fs.css({
                    'transform': 'scale(' + scale + ')',
                    'position': 'relative'
                });
                next_fs.css({
                    'left': left,
                    'opacity': opacity
                });
            },
            duration: 0,
            complete: function() {
                current_fs.hide();
                animating = false;
            },
            //this comes from the custom easing plugin
            easing: 'easeInOutBack'
        });

    }

});


$(".previous").click(function() {
    if (animating) return false;
    animating = true;
    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();
    $("#shopselector").show();
    $("#shopbar").empty();
    $(".boxtitle").remove();

    //de-activate current step on progressbar
    $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
    console.log(previous_fs)
    //show the previous fieldset
    previous_fs.show();
    //hide the current fieldset with style
    current_fs.animate({
        opacity: 0
    }, {
        step: function(now, mx) {
            //as the opacity of current_fs reduces to 0 - stored in "now"
            //1. scale previous_fs from 80% to 100%
            scale = 0.8 + (1 - now) * 0.2;
            //2. take current_fs to the right(50%) - from 0%
            left = ((1 - now) * 50) + "%";
            //3. increase opacity of previous_fs to 1 as it moves in
            opacity = 1 - now;
            current_fs.css({
                'left': left
            });
            previous_fs.css({
                'transform': 'scale(' + scale + ')',
                'opacity': opacity
            });
        },
        duration: 0,
        complete: function() {
            current_fs.hide();
            animating = false;
        },
        //this comes from the custom easing plugin
        easing: 'easeInOutBack'
    });
});

$(".submit").click(function() {
    return false;
})


$('#jarsearch').on('input', function() {
    var search = $('#jarsearch').val();
    $('.opval').remove()
    var url = '/shop/select/';
    var data = {
        jar: search
    }

    $.ajax({
        type: "GET",
        url: url,
        data: data,
        success: function(data) {


            if (typeof data !== 'string') {
                jQuery.each(data, function(i, val) {
                    jQuery.each(val, function(i, val) {
                        $('#jarlist').append("<option class='opval' value='" + val['jar_number'] + "'>" + val['jar_name'] + "</option>");
                    });
                });
            }

        }
    });

});


$("#JarSearchForm").submit(function(e) {
    var form = $(this);
    var url = '/shop/select/';
    $.ajax({
        type: "GET",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data) {
            if (data['models_to_return'].length > 0) {
                window.location.href = "/shop/"
            } else {
                $('#alert').append('<div class="alert alert-danger" role="alert"> The Jar you selected in not available. Select your Jar in <a href="/album" class="alert-link">Jar Albums</a></div>')

            }

        }
    });

    e.preventDefault(); // avoid to execute the actual submit of the form.
});


$("#pay").submit(function(e) {
    e.preventDefault();
    var form = $(this);
    var url = '/shop/tocheckout/';
    $.ajax({

        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function(data) {
            window.location.href = data
        }
    });


});

