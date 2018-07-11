$(document).ready(function() {
    console.log("Hello");
    $('.thumbs').click(function (event) {
        console.log("here");
        console.log($( this ).attr('id'));
        if($( this ).text() == "Thumbs up"){
            $( this ).text("Thumbs down")
        } else {
            $( this ).text("Thumbs up")
        }
    });
});