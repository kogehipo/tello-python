import socket   # UDP通信のため
from time import sleep
import curses   # これは端末エミュレーションのようなライブラリ

INTERVAL = 0.2

def report(str):
    stdscr.addstr(0, 0, str)
    stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()  # 初期化
    curses.noecho()            # エコーなし
    curses.cbreak()            # 入力はバッファされない

    # ステータス受信用のUDPサーバの設定
    local_ip = ''       # '0.0.0.0'と同じ意味．すなわち「全てのネットワークインターフェイスを使う」
    local_port = 8890   # ステータス受信は8890ポート
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ソケットを作成
    socket.bind((local_ip, local_port))   # サーバー側はバインドが必要

    # コマンド送信用の設定
    tello_ip = '192.168.10.1'  # Telloのipアドレス
    tello_port = 8889          # コマンドは8889ポートへ送る
    tello_adderss = (tello_ip, tello_port)  # アドレスを作成

    # 最初に"command"を送ってSDKモードを開始する
    socket.sendto('command'.encode('utf-8'), tello_adderss)

    # Ctrl+Cが押されるまで繰り返す
    try:
        index = 0    # ループ回数
        while True:
            index += 1
            response, ip = socket.recvfrom(1024) # 受信は最大1024バイトまで．受信結果はresponse変数に入る
            if response == 'ok':  # 受信データがokだけだったら再ループ
                continue
            # 受信データを加工
            out = response.decode('utf-8')  # 戻り値はバイナリーなのでデコードしてstr型に変換
            out = out.replace(';', ';\n')
            out = 'Tello State:\n' + out
            report(out)
            sleep(INTERVAL)
    except KeyboardInterrupt:   # Ctrl+Cが押された時の終了処理
        curses.echo()
        curses.nocbreak()
        curses.endwin()


