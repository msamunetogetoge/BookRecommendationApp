// 読みたい本や、お気に入りの作家で×押す->削除可能状態->削除
$(".clear_button").click(function () {
    if ($(this).parents('li').hasClass("pre_clear")) {
        // ajax でpost送信して削除
        $(this).parents("form").submit();
    } else {
        // li要素にpre_claerクラスを付与
        $(this).parents('li').addClass("pre_clear");
    }
});

// マウスが離れたら削除不可状態に戻す
$("li").mouseleave(function () {
    if ($(this).hasClass("pre_clear")) {
        $(this).removeClass("pre_clear");
    }
});

// not_read_modalが開く時にデータを渡す
$("#not_read_modal").on('show.bs.modal', function (event) {
    //モーダルを開いたボタンを取得
    var button = $(event.relatedTarget);
    // データ渡す
    $("#title_textbox").val(button.data("title"));
    $("#readdate_textbox").val(create_today());
    $("#thoughts_textbox").val(button.data("thoughts"));
    $("#title_textbox").attr('readonly', true);
});

// 既読本をクリックした時に、モーダルを開く
$(".readdata").click(function (event) {
    var button = $(this).parent().find("#readdata_update");
    button.click();
});

// 感想登録エリアのバリデーション(順番がおかしくなるので指定しなおす)
var textbox = $(".thoughts_textbox");
textbox.off('blur');
textbox.on('blur', validate_input_length("thoughts_textbox", 300, true));
textbox.on('blur', check_valid);


// input type=date に渡せる今日のデータ作成
function create_today() {
    var today = new Date();
    today.setDate(today.getDate());
    var yyyy = today.getFullYear();
    var mm = ("0" + (today.getMonth() + 1)).slice(-2);
    var dd = ("0" + today.getDate()).slice(-2);
    var now = yyyy + '-' + mm + '-' + dd;
    return now;
}

// 感想登録モーダルの感想長さバリデーション結果で登録ボタンを使えなくする
function check_valid() {
    var ok_flag = false;
    if ($(".thoughts_textbox").hasClass("is-valid")) {
        ok_flag = true;
    }

    if (ok_flag) {
        $("#thoughts_modal_submit_button").prop("disabled", false);
    }
    else {
        $("#thoughts_modal_submit_button").prop("disabled", true);
    }
};

// 感想文の長さチェック関数
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