## 2022年度RDクラブ・ECRチーム

チームによるTELLOテスト用リポジトリです。使用しているのはTELLO-EDUです。

## 環境設定

このリポジトリの内容を動作させるための手順です。

1. Windowsの場合はWSLでUbuntuを使ってください。
    Macの場合はターミナルを使います。

2. Python3が動く環境を作成してください。
    Python3.9を標準にします。（後で変更するかもしれません）
    virtualenv等で仮想環境を作ることを推奨します。
    以下、コマンドプロンプトで (env) と記載されているのは、
    "env" という名前の仮想環境の中であることを示します。

3. GitHubからリポジトリをクローンします。
```
    $ git clone https://github.com/kogehipo/tello
```
4. 仮想環境に入ります。（ディレクトリ構成によっては(3)、(4)の順番は変わります）
```
    $ source env/bin/activate
    (env) $
```
5. クローンしたディレクトリに移動して、pip3で必要なライブラリをインストールします。
```
    (env) $ cd tello
    (env) $ pip3 install -r requirement.txt
```
6. "exXX"で始まるディレクトリがそれぞれサンプルです。

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

基本的にex01と同じ内容です。コマンドはソースコードとは別のファイルcommand.txtに記述し、ひとつずつTELLOに送信します。実行はこのようにします。
```
    (env) $ python3 tello_test.py command.txt
```
やはりコマンドが動作しないことが頻繁にあります。コマンドのレスポンスを待っている間にタイム・アウトしてしまいます。下位にlogという名前のディレクトリを作っておくとログが保存されます。

## ex04-コマンド入力で制御

参考にしたページ

https://qiita.com/takanorimutoh/items/759734f17321344615b6

TELLOに送るコマンドを随時キーボードからタイプする。最初に "command" が必要。
```
    (env) $ python3 Tello3.py


    Tello Python3 Demo.

    Tello: command takeoff land flip forward back left right 
        up down cw ccw speed speed?

    end -- quit demo.

    command      ←これを忘れると動作しない
    ok
    takeoff     ←離陸
    ok
    forward 50
    ok
    left 50
    ok
    land
    ok
    ^C
```
ex01、ex03と同じはずだが、これはうまく行く。何が違うかは不明。

## メモ

役に立ちそうな記事をメモっておきます。

https://www.ryzerobotics.com/jp

TELLO公式ページ

https://algorithm.joho.info/programming/python/tello-python-command/

TkinterでPC上に制御用のUIを作った例。

https://midoriit.com/2018/05/python%E3%81%AB%E3%82%88%E3%82%8B%E3%83%89%E3%83%AD%E3%83%BC%E3%83%B3%E3%80%8Ctello%E3%80%8D%E3%81%AE%E5%88%B6%E5%BE%A1.html

Pydroid3を使ってスマホから制御できるようにしています。

https://qiita.com/Mitsu-Murakita/items/b86ad79d3590adb3b5b9

M5StackでTELLOを制御したようです。

https://kodamap.hatenablog.com/

TELLOで物体追跡しています。
