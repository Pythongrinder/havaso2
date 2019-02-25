// this is the id of the form
$("#subscribe").submit(function(e) {
e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = $(this);
    var url = form.attr('action');
    var data = form.serialize()
    $('#alerts').empty()
    $.ajax({
           type: "POST",
           url: url,
           data: data,
           success: function(data)
           {

                $('#alerts').append(
        '<div class="alert alert-info" role="alert">' +
            '<button type="button" class="close" data-dismiss="alert">' +
            '&times;</button>' + data + '</div>').hide().fadeIn(2000);


           }
         });


});