// this is the id of the form
$("#addwishlist").click(function() {

    var form = $(this);
    var url = form.attr('action');
    var data = {status: status}

    $.ajax({
           type: "GET",
           url: url,
           data: data,
           success: function(data)
           {
               alert(data);
           }
         });


});