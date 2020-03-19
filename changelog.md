# WARBotとは
Discordに生息しているBot。

[限界大会](https://apps.m86.work/genkai/)やその他サービスが動いています。

追加・コマンドリスト等に関しては[公式サイト](https://apps.m86.work/warbot/)を参照。

更新履歴のコマンドの詳細はコマンドリストで見れます。

## 動作環境
言語：`Python`

Pythonバージョン：`Python 3.7.3`

OS：`Ubuntu 18.04.2 LTS 64bit`

## 開発環境
エディター：`Microsoft VisualStudio Code`

OS：`Windows 10 Pro 64bit`

## Bot情報
稼働時間：`24Hour`

バージョン：`Beta4.1.1`

コマンドリスト：[WARBotコマンドリスト](https://apps.m86.work/warbot/commandlist.html)

# 更新履歴
- beta4.1.1 (2019/06/05)
  - コマンド追加
    - `/changelog` 更新履歴を確認するコマンド

----

- beta4.0.1 (2019/06/05)
  - バグ修正
    - 限界大会終了時に終了メッセージが大量投稿されるバグの修正

----

- [beta4.0](https://dev.m86.work/notice/post/1.html) (2019/02/24)
  - バグ修正
    - チャレンジ機能が正常終了しないバグ
  - コマンドの追加
    - `/get-sym`
    - `/get-tweetid`
    - `/restart`
    - `/get-reverse`
    - `/doners`
    - `/ジョウタ`

----

- これ以前のバージョンに関しては[こちら](https://scrapbox.io/warbot/%E6%9B%B4%E6%96%B0%E5%B1%A5%E6%AD%B4)

# バグ
- [x] 限界大会終了時にバグ発生
  - Beta4.0.1で修正。
- [ ] 限界大会お題投稿時の文字コード問題
  - 仕様上UTF-8しか読み込めないので、それに強制する必要あり。

# 開発中の機能

- [ ] 限界大会 自動ポートフォリオ作成機能
  - [x] ツイート情報の取得
  - [ ] ツイート動画の取得
  - [ ] 高画質データの取得
  - [ ] ページ作成機能
- [ ] ポイント送金機能
- [ ] 賽銭機能追加要素
- [ ] 限界イラスト大会
- [ ] 限界写真大会

- [ ] パンツの色出力機能
  - [ ] カラーコードで出力しよう
- [x] `/changelog`の追加
  - `beta 4.1.1`で追加