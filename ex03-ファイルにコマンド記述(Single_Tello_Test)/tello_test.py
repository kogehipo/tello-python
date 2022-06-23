from tello import Tello
import sys
from datetime import datetime
import time

start_time = str(datetime.now())

# 引数にコマンドを書いたファイル名を指定する
file_name = sys.argv[1]

# コマンドファイルを読む
f = open(file_name, "r")
commands = f.readlines()

tello = Tello()
for command in commands:   # コマンドを1行づつ実行
    if command != '' and command != '\n':
        command = command.rstrip()
        print('\n')

        # delayコマンドはTelloに送るのではなくsleep()を使う
        if command.find('delay') != -1:
            sec = float(command.partition('delay')[2])
            print('delay %s' % sec)
            time.sleep(sec)
            pass
        # delay以外のコマンドはTelloに送る
        else:
            tello.send_command(command)

# ここからはログを保存する処理
log = tello.get_log()

out = open('log/' + start_time + '.txt', 'w')
for stat in log:
    stat.print_stats()
    str = stat.return_stats()
    out.write(str)
