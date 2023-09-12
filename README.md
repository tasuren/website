[![Discord](https://img.shields.io/discord/777430548951728149?label=chat&logo=discord)](https://discord.gg/kfMwZUyGFG)
# 私のウェブサイト
このリポジトリの所有者の[ウェブサイト](https://tasuren.jp/)です。  
ウェブフレームワークにAstroを使用していて、ブログページはmicroCMSとの連携によって実現しており、ウェブサイトはJamstackな構成となっています。

## 必要要件
開発する場合、npmではなくpnpmを使ってください。  
ビルドのみの場合は、npmで構いません。

## ビルド方法
`npm i`または`pnpm i`で依存関係をインストールした後、`npm build`または`pnpm build`でビルドを開始できます。  
### ブログページについて
ブログのデータはmicroCMSから読み込みます。  
もしブログページもビルドを行う場合は、`.env.template`を参考に`.env`ファイルを作成し、そこに必要な情報を書き込んでください。または`.env.template`にある変数通りに環境変数を設定してください。  
もしもmicroCMSのAPIキーが環境変数等に設定されててもmicroCMSを使いたくない場合、`NO_MICROCMS=1`の環境変数を設定して起動してください。そうすると、ブログが空の状態でビルドが始まります。（Unix系OSでの起動例：`NO_MICROCMS=1 pnpm start`）

## ライセンス
ここにあるコードは4条項BSDライセンスの下で提供されます。