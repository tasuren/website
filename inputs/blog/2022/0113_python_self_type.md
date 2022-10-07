^^
self.ctx.title = "Python メソッドの返り値の型をselfにする方法"
self.ctx.description = "Pythonでのクラスのメソッドで、`self`の型を表す方法について書かれた記事です。"
self.ctx.created_at = 1642204800
self.ctx.last_updated_at = 1642204800
^^

(元々この記事は、Qiitaにて公開をしていて、ここに移動しました。)  

例えばクラスのメソッドの返り値で`self`を返す時に、その`self`を表す型をアノテーションに付けたいということがあることがあります。  
例えば以下のようなユーザーを表す`User`クラスがあったとします。

```python
from typing import Optional

class User:
    "ユーザークラスです。"

    name: str
    id: int
    description: Optional[str] = None
    age: Optional[int] = None

    def __init__(self, name: str, id: int):
        self.name, self.id = name, id

    def update_profile(self):
        "ユーザーのプロフィールを取得してこのクラスを拡張します。"
        # ここでユーザーのプロフィールを取得する。(便宜上ここでは変数の代入で表します。)
        description = "I wanna be the guy!"
        age = 5
        # 新しいUserクラスのインスタンスを作り取得したデータを代入する。
        self.description = description
        self.age = age
        return self
```
このクラスのメソッド`update_profile`では、ユーザー情報を取得して、取得したデータを自分の属性`description`等に書き込みます。  
そしてインスタンスである`self`を返しています。  
別に`self`を返さなくても使えますがこうすることでこんなことができます。

```python
name, age = "tasuren", 16
print(f"{name}の説明:", User(name, age).update_profile().description)
```
もし`self`を返さないようにした場合はこうなります。

```python
name, age = "tasuren", 16
user = User(name, age)
user.update_profile()
print(f"{name}の説明:", user.description)
```
新しい変数を作ることになります。  
なんか気分悪いです。  
また、`self.__class__`から新しいインスタンスを作り、そのインスタンスを返すと言うメソッドを作るかもしれません。  
そういうような時に`self`の型を返り値の型として指定する方法です。

## 方法1 自分のクラスを返り値の型に指定する
これは単純で返り値の型に`"User"`と指定するだけです。  
なぜ文字列なのかというのは`User`が見つかりませんと言うエラーが発生してしまうからです。

```python
    def update_profile(self) -> "User":
```
ちなみにバージョン3.11では`"User"`ではなく`User`でもできるようになるそうです。  
そして3.11でなくても3.7以上なら`from __future__ import annotations`をやることで`User`のように指定することができます。
### デメリット
これは簡単でわかりやすいのですが、クラスを継承した場合は、`-> "User"`だとその継承したクラスを返すということにならないので、作っていくうちにアウトになってしまいます。  
例えば`User`クラスを継承したクラスである`Member`クラスを作り、そのクラスはチームのメンバー用のクラスとします。  
その`Member`クラスにはそのメンバーのチームの名前である`team`という属性があります  
この時`Member`クラスのメソッド`update_profile`を使いその返り値の`team`にアクセスしようとしたとします。  
(`Member(...).update_profile().team`)  
これはmypyはエラーとします。  
なぜなら返り値の型である`User`には`team`がありません。  
ですのでエディタの型補完にも`team`が表示されません。  
こういう時は`Union["User", "継承したクラス名"]`のように`typing.Union`を使い、`update_profile`メソッドをオーバーライドし、返り値の型を指定して`return super().update_profile() # type: ignore`をすると一応対処が可能です。  
ですがこれだと`# type: ignore`を使いますしめんどくさいのと気分悪いです。(個人の問題？)  
特に継承して使うクラスとして作ったクラスの場合はとってもめんどくさいです。  
ですので継承することがない場合に使うと良いやり方ですね。
## 方法2 `TypeVar`を使う。

```python
from typing import TypeVar

UserSelf = TypeVar("UserSelf", bound="User") # boundでベースを指定する。

# クラスの上らへんは省略

    def update_profile(self: UserSelf) -> UserSelf:
```

`self`は、`User`クラスをベースとしたものを示す`UserSelf`という型であることを示し、その`UserSelf`を返すとしています。  
`TypeVar`が具体的にどのように動作するのかは、ジェネリクスについて調べてから検索してみましょう。  
こうすれば方法1のデメリットが解決します。  
なのでもしクラスを継承する場合はこの方法を使った方が良いでしょう。

## 方法3 Python3.11を使う
Python3.11では、`self`の型を表す`Self`が、`typing`モジュールに追加されます。  
ただ、まだ安定版がリリースされていません。