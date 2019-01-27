

//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){



	current_fs = $(this).parent();
	next_fs = $(this).parent().next();


    var purpose = $('#purpose option:selected').val();

    if (purpose === 'Choose an option') {
// DOES NOT DO ANYTHING
 }



    else if (purpose === 'General') {
    console.log(purpose)
    animating = true;

    var url = '/shop/getcheckout/';
    var data = {purpose: purpose}

       $.ajax({
               type: "GET",
               url: url,
               data: data,
               success: function(data)
               {

               $("#shopselector option").each(function() {
                            $(this).remove();
                        });
                        $('#addq').find(':first-child').remove();


    if (typeof data !== 'string'){
                  jQuery.each(data, function(i, val) {
                    jQuery.each(val, function(i, val) {
                        next_fs.show();
                        console.log(val)
                 $('#shopselector').append("<option class='opval' value='" + val['ingredient'] + "'>" + val['ingredient'] + "</option>");


                                                     });
                                                });


                                                                 $('#shopbar').append("<input type='text' class='form-control' class='qt' placeholder='Quantity' name='quantity'> ");
                 $('#addq').append("<input type='submit' class='btn' value='Add More Ingredients' id='AddIngridient' name='quantity'>")

                                                     // ADD ANOTHER INPUT

$('#AddIngridient').click(function(event) {

event.preventDefault();


$( "#shopselector" ).clone().appendTo( "#shopbar" );
$('#shopbar').append("<input type='text' class='form-control qt' placeholder='Quantity' name='quantity'>");

});


                                }
               }
             });






/// WORKING

    } else if (purpose === 'Personal') {
    console.log(purpose)
    animating = true;
        var url = '/shop/getcheckout/';
    var data = {purpose: purpose}

       $.ajax({
               type: "GET",
               url: url,
               data: data,
               success: function(data)
               {


      $("#shopselector option").each(function() {
                                $(this).remove();
                            });
      $('#addq').find(':first-child').remove();

    if (typeof data !== 'string'){
                  jQuery.each(data, function(i, val) {
                    jQuery.each(val, function(i, val) {
                        next_fs.show();
                        console.log(val)
                  $('#shopselector').prepend("<option class='opval' value='" + val['keyword'] + "'>" + val['keyword'] + "</option>");

                                                     });
                                                });
                                }
               }
             });
    next_fs.show();







/// NOT WORKING YET
    } else {
    console.log(purpose)
        var url = '/shop/getcheckout/';
    var data = {purpose: purpose}

       $.ajax({
               type: "GET",
               url: url,
               data: data,
               success: function(data)
               {

    if (typeof data !== 'string'){
                  jQuery.each(data, function(i, val) {
                    jQuery.each(val, function(i, val) {
                        next_fs.show();
                        console.log(val)
                        $("#shopselector option").remove();
                 // $('#jarlist').append("<option class='opval' value='" + val['jar_number'] + "'>" + val['jar_name'] + "</option>");
                                                     });
                                                });
                                }
               }
             });
    animating = true;
    next_fs.show();

    }


    if (animating) {
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	//show the next fieldset
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'relative'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 0,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});

	}

});






$(".previous").click(function(){
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();

    $("#shopbar").empty();

	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

	//show the previous fieldset
	previous_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		},
		duration: 0,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	return false;
})



// OTHER FUNCTIONS




$('#jarsearch').on('input', function() {
    var search = $('#jarsearch').val();
    $('.opval').remove()
    var url = '/shop/select/';
    var data = {jar: search}



    $.ajax({
           type: "GET",
           url: url,
           data: data,
           success: function(data)
           {


if (typeof data !== 'string'){
              jQuery.each(data, function(i, val) {
              jQuery.each(val, function(i, val) {
              $('#jarlist').append("<option class='opval' value='" + val['jar_number'] + "'>" + val['jar_name'] + "</option>");
             });
            });
       }

           }
         });

});


// this is the id of the form
$("#JarSearchForm").submit(function(e) {


    var form = $(this);
    var url = '/shop/select/';
    $.ajax({
           type: "GET",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               if (data['models_to_return'].length > 0){

              window.location.href = "/shop/"
               } else {
 $('#alert').append('<div class="alert alert-danger" role="alert"> The Jar you selected in not available. Select your Jar in <a href="/album" class="alert-link">Jar Albums</a></div>')

               }

           }
         });

    e.preventDefault(); // avoid to execute the actual submit of the form.
});



// this is the id of the form
$("#subscribe").submit(function(e) {
e.preventDefault(); // avoid to execute the actual submit of the form.
alert("HELLO");
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize()

    $.ajax({
           type: "POST",
           url: url,
           data: data,
           success: function(data)
           {

                $('#alerts').append(
        '<div class="alert">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + data + '</div>');


           }
         });


});