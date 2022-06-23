2022年度RDクラブ・ECRチーム
TELLOテスト用リポジトリです。

## 環境設定

このリポジトリの内容を動作させるための手順です。

(1) Windowsの場合はWSLでUbuntuを使ってください。
    Macの場合はターミナルを使います。
(2) Python3が動く環境を作成してください。
    Python3.9を標準にします。（後で変更するかもしれません）
    virtualenv等で仮想環境を作ることを推奨します。
    以下、コマンドプロンプトで (env) と記載されているのは、
    "env" という名前の仮想環境の中であることを示します。
(3) GitHubからリポジトリをクローンします。
    $ git clone https://github.com/kogehipo/tello
(4) 仮想環境に入ります。（ディレクトリ構成によっては(3)、(4)の順番は変わります）
    $ source env/bin/activate
    (env) $
(5) クローンしたディレクトリに降りて、pip3で必要なライブラリをインストールします。
    (env) $ cd tello
    (env) $ pip3 install -r requirement.txt
(6) "exXX"で始まるディレクトリがそれぞれサンプルです。

## ex01-コマンドハードコーディング

参考にしたページ
https://deviceplus.jp/hi-tech/drone-on-auto-pilot-with-python-03/

TELLOのコマンドを直接送信しています。
コマンドが動作しないことが頻繁にありますが原因不明です。

## ex02-状態モニター

参考にしたページ
https://qiita.com/hsgucci/items/3327cc29ddf10a321f3c
https://github.com/dji-sdk/Tello-Python

飛びません。TELLOの内部のセンサー等の情報を表示するものです。
姿勢など検知していることがわかります。

## ex03-ファイルにコマンド記述(Single_Tello_Test)

参考にしたページ
https://qiita.com/hsgucci/items/3327cc29ddf10a321f3c
https://github.com/dji-sdk/Tello-Python

基本的にex01と同じ内容です。
コマンドはソースコードとは別のファイルcommand.txtに記述し、
ひとつずつTELLOに送信します。やはりコマンドが動作しないことが頻繁にあります。
下位にlogという名前のディレクトリを作っておくとログが保存されます。
