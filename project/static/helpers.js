function submitForm(id, parameters) {
    for (var key in parameters) {
        $(key).val(parameters[key]);
    }
    $('#' + id).submit();
}

$(document).ready(function () {
    $('[data-toggle="modal"]').click(function (e) {
        e.preventDefault();
        $.get($(this).attr('href'), function (data) {
            $("#modalWindowContent").html(data);
            $("#modalWindow").modal(show = true, backdrop = false);
        });

    });
});

function modifyDescription(id) {
    bootbox.prompt("What should be the new description of the photo?", function (result) {
        if (result !== null) {
            $("#photodesc" + id).val(result);
            $("#modifydesc" + id).submit();
        }
    });
}