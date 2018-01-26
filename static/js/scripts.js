$(function(){
// open the modal
$('.launch-modal').on('click', function(e){
e.preventDefault();
$( '#' + $(this).data('modal-id') ).modal();
}); // reload the modal contents when it is closed
$('#' + $(this).data('modal-id')).on("hidden.bs.modal", function () {
var url = $('.video-frame').attr('src');
$('.video-frame').attr('src', '');
$('.video-frame').attr('src', url);
});
});