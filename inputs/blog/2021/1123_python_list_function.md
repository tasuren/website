^^
self.ctx.title = "Pythonのリストの値を`for`で回し、その値を関数で使う時に、全て同じ値になった件について。"
self.ctx.description = "Pythonのリストの値を`for`で回し、その値を関数で使う時に、全て同じ値になって関数で使われた件について書いた記事です。"
self.ctx.created_at = 1637625600
self.ctx.last_updated_at = 1637625600
^^

以下のようなコードがあったとする。
```python
numbers = [1, 2, 3]
functions = []

for i in numbers:
    def new():
        print(i)
    functions.append(new)

for function in functions:
    function(i)
```
このコードを作った人は以下の`望んだ出力`のように出力されることを望んでいました。  
一見普通に動くようにみえます。でも、これが実は動かない！
```python
# 望んだ出力
1
2
3
# 実際の出力
3
3
3
```
## 調べてみる
まずは追加した関数のIDが同じかどうかを組み込み関数の`id`で確かめてみる。  
`print(id(function))`を最後の`for function in functions:`の中に入れる。
### 出力1
```
4155492504
3
4156643264
3
4155172800
3
```
あっれえ？ちゃんと別のIDになってる、別の関数になってるのにどうして3になっちゃうの？  
ん？`for`でとった変数`i`のIDはどうなってるんだ？  
ってことで`print(id(i))`を最初の`for`の中に置いてそっちのIDも調べてみる。
### 出力2
```
4160119552
4160119568
4160119584
3
3
3
```
ですよねー、やっぱ`for`で回してるだけだしそうなるよねー。  
じゃあなんで全部3なんだ？  
ん？もしかして関数の中の`i`が同じ...!?  
ってことで`print(id(i))`を関数`new`の中に入れてもう一回調べる。
### 出力3
```
4160119584
3
4160119584
3
4160119584
3
```
なんと！全部`for`で回したものの最後のものになっているではないか！
## 理由
`for`でまわす時に使う変数は`for`が置かれてるスコープで作られる。  
そしてそのスコープでできた関数内でその変数が使われる際その変数を参照する。  
あくまでその関数内専用の変数が新しく作られるわけではなく、変数名から既にある変数を参照するだけということになる。(多分...?)  
なので関数を使う際に参照した変数`i`には`for`の最後である3が入っているから3が出力された。
## 解決
三文字付け加えるだけで解決しました。
### コード
```python
numbers = [1, 2, 3]
functions = []

for i in numbers:
    def new(i=i):
        print(i)
    functions.append(new)

for function in functions:
    function(i)
```
関数にキーワード引数として`i=i`を付け加えただけ。  
たったこれだけで動く。  
関数を作る際に`i`に入っている値をデフォルトとするキーワード引数を作り、関数実行時にそのキーワード引数から新しく変数を作るようにすることで解決した。