^^
self.ctx.title = "iSHのPythonで一部ライブラリを入れられない問題"
self.ctx.description = "tasurenのブログの方針を軽くまとめてみた。"
self.ctx.created_at = 1659056280.9349816
self.ctx.last_updated_at = 1659059414.4900255
^^
これは、iSHにてyarlやujson等のライブラリをインストールする際に、エラーが発生してインストールできない時の対処法をまとめたものです。  
他のLinuxのディストリビューションでも起こり得ることだと思います。  
このエラーは必要なライブラリが不足してることにより発生しています。
## python.hがない
エラー文の下の方に`<python.h>`とある場合です。  
この場合はPythonの開発ライブラリがない(または見つからない状態)から発生しています。  
その開発ライブラリは、大抵`python-dev`という名前でパッケージマネージャーからインストールが可能です。  
iSHの場合は`apk add python3-dev`でインストールが可能です。
## limits.hがない
エラー文の下の方に`<limits.h>`とある場合です。  
この場合はmuslというライブラリがインストールされていないまたは見つからない状態です。  
iSHでは`apk add musl-dev`でインストールができます。
## エラー文の例文
これはGoogleにひっかかりやすくするためのものです。  
これで他のこれらのエラーと同じようなエラーで苦しんでる人も少しはハッピーになれるかもしれません。

```python
ERROR: Command errored out with exit status 1:
   command: /usr/bin/python3 /usr/lib/python3.9/site-packages/pip/_vendor/pep517/_in_process.py build_wheel /tmp/tmphtyy_2mz
       cwd: /tmp/pip-install-ejpric_d/multidict_32c7ab8c36eb4ba599afa9775cb14c4d
  Complete output (42 lines):
  *********************
  * Accelerated build *
  *********************
  running bdist_wheel
  running build
  running build_py
  creating build
  creating build/lib.linux-i686-3.9
  creating build/lib.linux-i686-3.9/multidict
  copying multidict/_multidict_py.py -> build/lib.linux-i686-3.9/multidict
  copying multidict/_abc.py -> build/lib.linux-i686-3.9/multidict
  copying multidict/__init__.py -> build/lib.linux-i686-3.9/multidict
  copying multidict/_multidict_base.py -> build/lib.linux-i686-3.9/multidict
  copying multidict/_compat.py -> build/lib.linux-i686-3.9/multidict
  running egg_info
  warning: no previously-included files matching '*.pyc' found anywhere in distribution
  warning: no previously-included files found matching 'multidict/_multidict.html'
  warning: no previously-included files found matching 'multidict/*.so'
  warning: no previously-included files found matching 'multidict/*.pyd'
  warning: no previously-included files found matching 'multidict/*.pyd'
  no previously-included directories found matching 'docs/_build'
  writing manifest file 'multidict.egg-info/SOURCES.txt'
  copying multidict/__init__.pyi -> build/lib.linux-i686-3.9/multidict
  copying multidict/_multidict.c -> build/lib.linux-i686-3.9/multidict
  copying multidict/py.typed -> build/lib.linux-i686-3.9/multidict
  creating build/lib.linux-i686-3.9/multidict/_multilib
  copying multidict/_multilib/defs.h -> build/lib.linux-i686-3.9/multidict/_multilib
  copying multidict/_multilib/dict.h -> build/lib.linux-i686-3.9/multidict/_multilib
  copying multidict/_multilib/istr.h -> build/lib.linux-i686-3.9/multidict/_multilib
  copying multidict/_multilib/iter.h -> build/lib.linux-i686-3.9/multidict/_multilib
  copying multidict/_multilib/pair_list.h -> build/lib.linux-i686-3.9/multidict/_multilib
  copying multidict/_multilib/views.h -> build/lib.linux-i686-3.9/multidict/_multilib
  running build_ext
  creating build/temp.linux-i686-3.9
  creating build/temp.linux-i686-3.9/multidict
  gcc -Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -fomit-frame-pointer -g -fno-semantic-interposition -fomit-frame-pointer -g -fno-semantic-interposition -fomit-frame-pointer -g -fno-semantic-interposition -DTHREAD_STACK_SIZE=0x100000 -fPIC -I/usr/include/python3.9 -c multidict/_multidict.c -o build/temp.linux-i686-3.9/multidict/_multidict.o -O2 -std=c99 -Wall -Wsign-compare -Wconversion -fno-strict-aliasing -pedantic
  In file included from multidict/_multidict.c:1:
  /usr/include/python3.9/Python.h:11:10: fatal error: limits.h: No such file or directory
     11 | #include <limits.h>
        |          ^~~~~~~~~~
  compilation terminated.
  error: command '/usr/bin/gcc' failed with exit code 1
  ----------------------------------------
  ERROR: Failed building wheel for multidict
ERROR: Could not build wheels for yarl, multidict which use PEP 517 and cannot be installed directly
```