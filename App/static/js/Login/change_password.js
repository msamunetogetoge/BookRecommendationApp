// passwordとpassword_againが一致しているかの判定
var elm_pass = $('#pass_textbox');
var elm_confirm = $('#pass_textbox_again');

// 一回目のパスワードからフォーカスが外れたら確認パスワードにフォーカスする
elm_pass.on('blur', function () {
    elm_confirm.focus();
});
//確認パスワード入力のフォーカスを失ったとき（Blur）のイベントリスナー
elm_confirm.on('blur', function () {
    // ok
    if (elm_pass.val() === "" && elm_confirm.val() === "") {
        elm_confirm.removeClass("is-invalid");
        elm_pass.removeClass("is-invalid");
        elm_confirm.removeClass("is-valid");
        elm_pass.removeClass("is-valid");
    }
    else if (elm_pass.val() === elm_confirm.val()) {
        elm_confirm.removeClass("is-invalid");
        elm_confirm.addClass("is-valid");
    }
    // nvalid
    else {
        elm_confirm.removeClass("is-valid");
        elm_confirm.addClass("is-invalid");
    }
    check_password_confirm("pass_textbox_again", "password_button");
});
// パスワードの一致が確認できるまではパスワード変更ボタンは使えなくする
function check_password_confirm(pass_textbox_again, password_button) {
    if ($("#" + pass_textbox_again).val() === "") {
        $("#" + password_button).prop("disabled", true);
    }
    else if ($("#" + pass_textbox_again).hasClass("is-valid")) {
        $("#" + password_button).prop("disabled", false);
    }
    else {
        $("#" + password_button).prop("disabled", true);
    }
}