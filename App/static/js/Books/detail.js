// 感想登録エリアのバリデーション(順番がおかしくなるので指定しなおす)
var textbox = $(".thoughts_textbox");
textbox.off('blur');
textbox.on('blur', validate_input_length("thoughts_textbox", 300, true));
textbox.on('blur', check_valid);

// 感想登録modalにデータを渡す
$("#not_read_modal").on('show.bs.modal', function (event) {
    //モーダルを開いたボタンを取得
    var button = $(event.relatedTarget);
    // データ渡す
    $("#title_textbox").val(button.data("title"));
    $("#readdate_textbox").val(create_today());
    $("#thoughts_textbox").val("");
});

// 検索結果をスライド表示する
$('.multiple-items').slick({
    dots: true,
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 3,
    prevArrow: '<div class="slick-prev"></div>',
    nextArrow: '<div class="slick-next"></div>',
    centerPadding: '30px',
    responsive: [
        {
            breakpoint: 768,
            settings: {
                arrows: false,
                centerMode: false,
                centerPadding: '40px',
                slidesToShow: 2,
                slidesToScroll: 2,
            }
        },
        {
            breakpoint: 480,
            settings: {
                arrows: false,
                centerMode: true,
                centerPadding: '40px',
                slidesToShow: 1,
                slidesToScroll: 1,
            }
        }
    ]
});

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

// 今日の日付データを作成する
function create_today() {
    var today = new Date();
    today.setDate(today.getDate());
    var yyyy = today.getFullYear();
    var mm = ("0" + (today.getMonth() + 1)).slice(-2);
    var dd = ("0" + today.getDate()).slice(-2);
    var now = yyyy + '-' + mm + '-' + dd;
    return now;
}

