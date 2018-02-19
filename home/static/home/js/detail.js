$(document).ready(function() {
    $('#imageGrid img').click(function(){
        $('#overlay').show();
        $('#image-container').append("<img src="+ this.src + ">");
    });
    
    $('#overlay').click(function(){
        $('#image-container').empty();
        $('#overlay').hide();
    });
});