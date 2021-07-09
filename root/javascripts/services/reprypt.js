/* Reprypt by tasuren
注意：実はこのjavascriptはRepryptのコードではありません。
tasurenがjavascript版のRepryptライブラリを作るのがめんどくさいため、tasurenの管理しているRTというDiscordのBotのウェブサイトにつくったRepryptのAPIを叩いています。
いつかjavascript版も時間がある時作りたいと思うtasurenだった。
(ちびまるこちゃんのあのナレーターさんのあれ風)
*/


$(function() {
    // リクエストして結果を表示する関数
    function Reprypt(mode, original, target, key) {
	// ボタンを無効にしてNow loading...を表示する。
	enbtn = $("#repryptEncrypt");
	debtn = $("#repryptDecrypt");
	enbtn.attr("disable", true);
	debtn.attr("disable", true);
	$("#repryptNow").show();
	// リクエストするデータを作る。
	var data = {
	    mode: mode,
	    content: original.val(),
	    password: key
	};
	// リクエストする。
	$.ajax({
	    url: "https://rt-bot.com/api/reprypt",
	    type: "post",
	    data: JSON.stringify(data),
	    dataType: "JSON",
	    success: function(data) {
		target.text(data.result);
		target.val(data.result);
	    },
	    error: function() {
		alert("失敗しました。短時間による実行またはパスワードの間違いなどの原因が考えられます。");
	    },
	    complete: function() {
		// ボタンを有効にしてNow loading...を消す。
		enbtn.attr("disable", false);
		debtn.attr("disable", false);
		$("#repryptNow").hide();
	    }
	});
    };


    $("#repryptNow").hide();


    $("#repryptEncrypt").click(function() {
	Reprypt("en", $("#repryptInput"),
		$("#repryptOutput"), $("#repryptKey").val());
    });

    $("#repryptDecrypt").click(function() {
	Reprypt("de", $("#repryptOutput"),
		$("#repryptInput"), $("#repryptKey").val());
    });
});
