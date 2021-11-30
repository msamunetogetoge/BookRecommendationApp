function validate_input_length(classname, max_length, allow_zenkaku = true) {
    if (allow_zenkaku) {
        $("." + classname).on('blur', function () {
            var input_length = $(this).val().length;
            if (input_length > max_length) {
                $(this).removeClass("is-valid");
                $(this).addClass("is-invalid");
            }
            else if (input_length === 0) {
                $(this).removeClass("is-valid");
                $(this).removeClass("is-invalid");
            }
            else {
                $(this).removeClass("is-invalid");
                $(this).addClass("is-valid");
            }
        });
    }
    else {
        $("." + classname).on('blur', function () {
            var input_length = $(this).val().length;
            var input_byte_lengh = encodeURI($(this).val()).replace(/%../g, "*").length;
            if (input_length != input_byte_lengh || input_length > max_length) {
                $(this).removeClass("is-valid");
                $(this).addClass("is-invalid");
            }
            else if (input_length === 0) {
                $(this).removeClass("is-valid");
                $(this).removeClass("is-invalid");
            }
            else {
                $(this).removeClass("is-invalid");
                $(this).addClass("is-valid");
            }
        });
    }

};

// ロード完了時に、入力文字列長さに制限を付ける
window.onload = function () {
    validate_input_length("id_textbox", 16, false);
    validate_input_length("password_textbox", 32, false);
    validate_input_length("name_textbox", 64, true);
    validate_input_length("email_textbox", 64, true);
    validate_input_length("thoughts_textbox", 300, true);
};

