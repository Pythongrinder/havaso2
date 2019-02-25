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

$("#viewwishlist").click(function(){
    $("#wishlisttable").empty()
    var url = '/wishlist/view/';
    $.ajax({
         type: "GET",
         url: url,
         dataType: "json",
         data: 'view=view', // serializes the form's elements.
         success: function(data){
                for (x in data[0]) {
                wishlistItems = '<tr> <td><img width="50px" onclick="large.call(this)" src="/media/'+ data[0][x]['fields']['jar_image'] +'">' +
               '</td><td>'+ data[0][x]['fields']['jar_name'] +' <p>Decorated by '+ data[0][x]['fields']['decorator'] +' </p></td> ' +
               '<td class="text-right"><button value="'+ data[0][x]['fields']['jar_number'] +'" class="btn btn-sm btn-danger removejar">Remove</button>'+
               '<button value="'+ data[0][x]['fields']['jar_number'] +'" class="btn btn-sm btn-success buyjar ml-1">Buy</button></td></tr>';
                $("#wishlisttable").append(wishlistItems)
                }
                                    }
         });
});

var large = function() {
   var src = $(this).attr("src");
   console.log(src)
   $('body').append('<div class="modal-overlay"></div><div class="modal-img"><img height="300px" width="300px" src="'+src+'" /></div>')
}
$('body').on('click', '.modal-overlay', function () {
    $('.modal-overlay, .modal-img').remove();
});





// When loading the wishlist view from add to the wishlist.

$('#wishlist').on('hidden.bs.modal', function () {
  // Load up a new modal...
  $('#viewwishlist').click()
})



// this is the id of the form
$(".sendwishlistemail").submit(function(e) {

    var form = $(this);
    var url = '/wishlist/emailwishlist/';
    $(".wishlist-alert").removeAttr("hidden").append('<p class="text-center">Wish list email sending!</p>');
    $(".wishlist-alert").fadeIn( 400 );

    $.ajax({

           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
           if (data === "Empty") {

           $(".wishlist-alert").empty();
           $(".wishlist-alert").append('<p class="text-center alert-text">The wish list is Empty!</p>');
           $(".wishlist-alert").delay( 1500 ).fadeOut( 800 )

           } else {
           $(".wishlist-alert").empty();
           $(".wishlist-alert").append('<p class="text-center alert-text">Wish list email sent!</p>');
           $(".wishlist-alert").delay( 2500 ).fadeOut( 800 )
           }

           }
         });

    e.preventDefault(); // avoid to execute the actual submit of the form.
});


// this is the id of the form
$(document).on('click', '.buyjar', function() {

    var url = '/wishlist/add/';
    var jarnumber = $(this).attr("value");
    var data = {buyjar: jarnumber}
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


// this is the id of the form
$(document).on('click', '.removejar', function() {
    $(this).closest("tr").remove();

    var url = '/wishlist/remove/';
    var jarnumber = $(this).attr("value");
    var data = {removejar: jarnumber}
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

