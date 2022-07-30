^^
self.ctx.title = "Dockerのインストールでapt_pkgが見つからない問題"
self.ctx.description = "Dockerのインストール時に`apt_pkg`というモジュールが見つからないというエラーが発生する問題を解決した話です。"
^^
Dockerを自分のUbuntu Serverにインストールしようとしたところよくわからんエラーで詰まった。  
その時の対処法を同じことになっている他の人のためにここに書き記す。  
注意：ここにあることを行なって何か損害が起きても自己責任とします。

まず最初にDockerのリポジトリを追加する際に以下のPythonのエラーがでた。

```shell
$ sudo add-apt-repository \                                 
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
Traceback (most recent call last):
  File "/usr/bin/add-apt-repository", line 12, in <module>
    from softwareproperties.SoftwareProperties import SoftwareProperties, shortcut_handler
  File "/usr/lib/python3/dist-packages/softwareproperties/SoftwareProperties.py", line 28, in <module>
    import apt_pkg
ModuleNotFoundError: No module named 'apt_pkg'
```
よくわからん...  
とりあえず、モジュールが見つからないということなので、`dist-packages`の中を見てみる。

```shell
$ cd /usr/lib/python3/dist-packages
$ ls apt_pkg*
apt_pkg.cpython-38-x86_64-linux-gnu.so

apt_pkg-stubs:
__init__.pyi
```
一応あるといえばあった。  
それなのになぜモジュールが見つからないというエラーが起きてしまうのだろうか...  
そこで色々ググってみたところ、この`apt_pkg.cpython-38-x86_64-linux-gnu.so`に似たものを見つけたが、どれも一文字違う名前だった。  
それが以下である。  
`apt_pkg.cpython-38m-x86_64-linux-gnu.so`  
どこが違うんだよって感じだけどよくみてみてください。  
> `38m`

`m`が自分のにはありません。  
もしやと思い名前に`m`を入れてみる。

```shell
$ sudo mv apt_pkg.cpython-38-x86_64-linux-gnu.so apt_pkg.cpython-38m-x86_64-linux-gnu.so
```
すると今度は別のエラーがでてしまった。

```shell
$ sudo add-apt-repository \                              
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
Traceback (most recent call last):
  File "/usr/bin/add-apt-repository", line 12, in <module>
    from softwareproperties.SoftwareProperties import SoftwareProperties, shortcut_handler
  File "/usr/lib/python3/dist-packages/softwareproperties/SoftwareProperties.py", line 68, in <module>
    from gi.repository import Gio
  File "/usr/lib/python3/dist-packages/gi/__init__.py", line 42, in <module>
    from . import _gi
ImportError: cannot import name '_gi' from partially initialized module 'gi' (most likely due to a circular import) (/usr/lib/python3/dist-packages/gi/__init__.py)
```
giが見つからないってなんやねん！  
色々調べたところ複数のバージョンのPythonが入っているとこうなるらしい。  
最近Pythonを複数バージョン入れるときにはpyenvを使うようにしていたが、Dockerをインストールしようとしているマシンにはpyenvを入れたことがなく、昔にPython3.8からPython3.9に手動でアップグレードした気がする。  
恐らく、元のPython3.8とPython3.9が競合しているのだろう。  
一体エラーが起きる時に使用しているPythonはどのバージョンのPythonなのだろうか。  
エラーが起きているファイルをnanoで開き、エラー箇所の手前に`print(__import__("sys").executable)`を置いて、どこにあるPythonを実行しているのかを表示するようにした。  
すると、`/usr/bin/python3`と表示された。`/usr/bin/python3`と実行するとPython3.9.5が起動した。  
となると、先ほどの`m`が名前になかったファイルは`cpython-38`とあったことから、これはPython3.8で実行されるべきなのだろう。  
(そもそもUbuntuに元から入ってたのがPython3.8な気がするし。)  
つまり、`/usr/bin/python3`からpython3.8が起動するようにすればうまくいくのではないだろうか。  
なお、`python3.8`とコマンドラインで実行するとPython3.8が起動する。  
てことで、`python3.8`がどこにあるのかを調べて、それをその`/usr/bin/python3`にコピーした。

```shell
$ which python3.8
/usr/bin/python3.8
$ sudo cp /usr/bin/python3.8 /usr/bin/python3
```
すると、やっとエラーもなく実行が成功した！

```shell
$ sudo add-apt-repository \            
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"
Get:1 https://download.docker.com/linux/ubuntu focal InRelease [57.7 kB]
Hit:2 http://jp.archive.ubuntu.com/ubuntu focal InRelease                                             
Get:3 http://jp.archive.ubuntu.com/ubuntu focal-updates InRelease [114 kB]
Get:4 https://download.docker.com/linux/ubuntu focal/stable amd64 Packages [17.6 kB]
Get:5 http://jp.archive.ubuntu.com/ubuntu focal-backports InRelease [108 kB]                                    
Get:6 http://jp.archive.ubuntu.com/ubuntu focal-security InRelease [114 kB]   
Get:7 http://jp.archive.ubuntu.com/ubuntu focal-updates/main amd64 Packages [1,992 kB]
Get:8 https://dlm.mariadb.com/repo/mariadb-server/10.6/repo/ubuntu focal InRelease [4,717 B]
Get:9 http://jp.archive.ubuntu.com/ubuntu focal-updates/universe amd64 Packages [926 kB]                
Get:11 https://dlm.mariadb.com/repo/maxscale/latest/apt focal InRelease [6,384 B]                    
Hit:10 https://downloads.mariadb.com/Tools/ubuntu focal InRelease                                                 
Fetched 3,340 kB in 1s (3,211 kB/s)
Reading package lists... Done
```
全く、Python3.9を二個インストールした昔の僕にはpyenvの存在を知ってもらいたいですね。  
みなさんもpyenv等を使ってインストールしましょう。()  
とりあえず無事解決した。