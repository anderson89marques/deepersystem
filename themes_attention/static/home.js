$(document).ready(function() {
    $('.thumbs').click(function (event) {
        var _id = $( this ).attr('id');
        var t_obj = {_id: _id}
        var t_up_bool = false
        if($( this ).text() == "Thumbs up"){
            t_obj.thumbs_up = 1
            $( this ).text("Thumbs down")
            t_up_bool = true
        } else {
            t_obj.thumbs_down = 1
            $( this ).text("Thumbs up")
            t_up_bool = false
        }
        var url = "/thumbs_attent"
        var posting = $.post( url, t_obj );
        posting.done(function( data ) {
            console.log('DONE');
            if(t_up_bool) {
                t_up = $("#thumbs_up" + _id).text()
                $("#thumbs_up" + _id).text(parseInt(t_up) + 1)
            } else{
                t_down = $("#thumbs_down" + _id).text()
                $("#thumbs_down" + _id).text(parseInt(t_down) + 1)
            }
          });
        
    });
});