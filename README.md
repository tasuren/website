[![Discord](https://img.shields.io/discord/777430548951728149?label=chat&logo=discord)](https://discord.gg/kfMwZUyGFG)
# 私のウェブサイト
このリポジトリの所有者のウェブサイトです。  
ウェブフレームワークにAstroを使用していて、ブログページはmicroCMSとの連携によって実現しており、ウェブサイトはJamstackな構成となっています。

## 必要要件
npmではなく、pnpmを使ってください。

## ビルド方法
`pnpm start`で、開発を開始できます。  
microCMSのAPIを使ってブログページもビルドを行う場合は、`.env.template`を参考に`.env`ファイルを作成し、そこに必要な情報を書き込んでください。  
もしも、一時的に`.env`に書き込んだサンプルデータを使ってブログページをビルドしたい場合は、`NO_MICROCMS`という環境変数を設定して起動してください。（Unix系での起動例：`NO_MICROCMS=1 pnpm start`）