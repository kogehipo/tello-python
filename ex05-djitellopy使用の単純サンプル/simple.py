from djitellopy import Tello

tello = Tello()

# Windows/WSLで実行したときに
# Exception: Did not receive a state packet from the Tello
# というエラーが発生するので False を追加した。
# 参照： https://github.com/damiafuentes/DJITelloPy/issues/149
# なお、Firewallが邪魔をするのでESET等のウイルス対策ソフトはアンインストールした。
#tello.connect()
tello.connect(False)

tello.takeoff()

'''
tello.move_left(100)
tello.rotate_clockwise(90)
tello.move_forward(100)
'''

tello.move_forward(100)
tello.move_right(100)
tello.move_back(100)
tello.move_left(100)

tello.land()
