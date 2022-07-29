^^
self.ctx.title = "JavaScriptのaタグのtargetを変更する。"
self.ctx.description = "JavaScriptのaタグのtargetを、リンクが外部サイトの場合のみ自動で`_blank`にするプログラムについて書かれているページです。"
^^
このウェブサイトの開発中にとあることに気づいた。  
というのも、リンクを開くと同じタブで開かれてしまいとても不便だということ。  
いや同じウェブサイトのリンクならいいんだけども、外部リンクの場合は新しいタブで開いてほしい。  
外部リンクの場合は、大抵の人が別のタブにしておいて、本来のウェブサイトを見ながらその外部サイトのタブを見るという感じにするだろう。(実際僕のやり方はこれだ。)  
そのため、外部リンクは新しいタブで自動で開いてくれればとても良い。  
てことで、JavaScriptを使用してこれを自動でやるようにしたいと思い、以下のコードを作成した。

```javascript
window.onload = function () {
  let url;
  for (element of document.getElementsByTagName("a")) {
    url = element.getAttribute("href");
    if (!url.startsWith(window.location.origin) && url.startsWith("http"))
      element.setAttribute("target", "_blank");
  };
};
```
## プログラム内容
まず最初に`for`で一つづつaタグの要素を取り出す。  
その後、URLがウェブサイトのリンクではないかつURLが`http`から始まるなら、そのaタグに`target`という属性を付けて、`_blank`をその属性に入れている。

## はまったこと
最初になぜか要素が取得できなくて少しハマったが、調べたところすぐ解決した。  
まだHTMLの読み込みが終わっていない状態でJavaScriptが実行されるせいで要素が取得できていなかった。  
これは、`window.onload`という読み込み終了時に呼ばれる属性に、aタグの更新を行う関数を入れることで解決した。  
これで読み込み終了時にaタグの更新を行う関数が実行されるようになるという。