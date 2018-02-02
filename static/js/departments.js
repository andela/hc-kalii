$(function () {
    $(".department-menu-remove").click(function() {
        var $this = $(this);

        $("#remove-department-form").attr("action", $this.data("url"));
        $(".remove-department-name").text($this.data("name"));
        $('#remove-department-modal').modal("show");

        return false;
    });

});
