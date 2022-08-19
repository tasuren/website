^^
self.ctx.title = "gitにて、権限エラーで`.git/objects`にアクセスできない問題について。"
self.ctx.description = "gitにて権限エラーが発生して`.git/objects`にアクセスできないというエラーが発生した。それの解決方法についてをまとめた。"
self.ctx.created_at = 1660903711.2600121
self.ctx.last_updated_at = 1660903711.2600121
^^
`git pull`等をしようとすると以下のようなエラーが発生してしまうことが起きた。  
```shell
$ git pull origin main
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
error: insufficient permission for adding an object to repository database .git/objects
fatal: failed to write object
fatal: unpack-objects failed
```
なお、`sudo`をすると成功する。  
エラーにある通りどうやら権限がないためこれが起きるようだ。  

## 解決方法
以下のように、`chown`コマンドを使用して、`.git`フォルダ内の全てのものの所有者を自分にすることで、この問題は解消された。  
```shell
$ sudo chown -R tasuren .git
```
