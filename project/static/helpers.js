function submitForm(id) {
    $('#' + id).submit();
}

function yesnodialog(title, message, callback) {
    bootbox.dialog({
        message: message,
        title: title,
        buttons: {
            no: {
                label: "No",
                className: "btn-default",
                callback: function () { }
            },
            yes: {
                label: "Yes",
                className: "btn-primary",
                callback: function () {
                    callback();
                }
            }
        }
    });
}

function confirmForm(title, message, id) {
    yesnodialog(title, message, function () {
        submitForm(id);
    });
}

function modifyAlbum() {
    bootbox.prompt("What should be the new name of the album?", function (result) {
        if (result !== null) {
            $("#albumname").val(result);
            $("#modifyalbum").submit();
        }
    });
}

function modifyLink(id) {
    bootbox.prompt("What should be the new link of the photo?", function (result) {
        if (result !== null) {
            $("#photolink" + id).val(result);
            $("#modifylink" + id).submit();
        }
    });
}

function modifyDescription(id) {
    bootbox.prompt("What should be the new description of the photo?", function (result) {
        if (result !== null) {
            $("#photodesc" + id).val(result);
            $("#modifydesc" + id).submit();
        }
    });
}