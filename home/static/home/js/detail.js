$(document).ready(function() {
    $('#imageGrid img').click(function(){
        $('#overlay').show();
        $('#overlay').append("<img src="+ this.src + " class=\"overlay-image\">");
    });
    
    $('#overlay').click(function(){
        $('#overlay').empty();
        $('#overlay').hide();
    });
});