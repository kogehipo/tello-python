#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is based on DJITelloPy,
# https://github.com/damiafuentes/DJITelloPy
# and Interface issued in April, 2022, CQ Publishing
#
# simple example demonstrating how to control a Tello using your keyboard.
# For a more fully featured example see manual-control-pygame.py
# 
# Use W, A, S, D for moving, E, Q for rotating and R, F for going up and down.
# When starting the script the Tello will takeoff, pressing ESC makes it land
#  and the script exit.


from djitellopy import Tello  # DJITelloPyのTelloクラスをインポート
import cv2      # OpenCVをインポート
#import math    # 
import time     # time.sleep()を使う

def main():

    ###########
    # 初期化
    ###########
    tello = Tello(retry_count=1)    # Telloクラスのインスタンス
                                    # 応答が来ないときのリトライは1（デフォルトは3）
    tello.RESPONSE_TIMEOUT = 0.01   # コマンド応答のタイムアウトは0.01（デフォルトは7）

    # Windows/WSL対応のためFalseを追加。（ex05を参照）
    #tello.connect()     # Telloへ接続
    tello.connect(False)     # Telloへ接続

    # 画像転送を行う
    tello.streamoff()   # いったん明示的にオフして、
    tello.streamon()    # オンする

    # BackgrounfFrameReadクラスのインスタンスを通して画像フレームを取得する
    frame_read = tello.get_frame_read()

    current_time = time.time()  # 現在時刻
    pre_time = current_time     # 前回、死活チェックを行った時刻
    motor_on = False                    # モーターOn/Offフラグ
    camera_dir = Tello.CAMERA_FORWARD   # 前方/下方カメラフラグ

    time.sleep(0.5)     # 通信安定するまで待つ

    print('Tello is starting...')

    ###########
    # ループ
    ###########
    try:    # コンソールでCtrl+Cが押されるまで永久ループ
        while True:

            # 画像を取得
            image = frame_read.frame
            # 画像サイズを縮小
            small_image = cv2.resize(image, dsize=(480,360))
            # 下向きカメラは90°回転して画像の上を前方にする
            if camera_dir == Tello.CAMERA_DOWNWARD:
                small_image = cv2.rotate(small_image, cv2.ROTATE_90_CLOCKWISE)
            # 画像を表示
            cv2.imshow("OpenCV Window", small_image)

            # OpenCVウインドウでキー入力を1ms待つ
            # このコマンドはOpenCVのウインドウでタイプすること。
            key = cv2.waitKey(1) & 0xff

            if key == 27:           # ESCだったらループ離脱
                break
            elif key == ord('t'):   # 離陸
                tello.takeoff()
            elif key == ord('l'):   # 着陸
                tello.land()
            elif key == ord('w'):   # 前進30cm
                tello.move_forward(30)
            elif key == ord('s'):   # 後退30cm
                tello.move_back(30)
            elif key == ord('a'):   # 左移動30cm
                tello.move_left(30)
            elif key == ord('d'):   # 右移動30cm
                tello.move_right(30)
            elif key == ord('e'):   # 時計回り30°
                tello.rotate_clockwise(30)
            elif key == ord('q'):   # 反時計回り30°
                tello.rotate_counter_clockwise(30)
            elif key == ord('r'):   # 上昇30cm
                tello.move_up(30)
            elif key == ord('f'):   # 降下30cm
                tello.move_down(30)
            elif key == ord('p'):   # ステータス表示
                print(tello.get_current_state())
            elif key == ord('m'):   # モーター始動/停止切り替え
                if motor_on == False:
                    tello.turn_motor_on()
                    motor_on = True
                else:
                    tello.turn_motor_off()
                    motor_on = False
            elif key == ord('c'):   # カメラ前方/下方切り替え
                if camera_dir == Tello.CAMERA_FORWARD:
                    tello.set_video_direction(Tello.CAMERA_DOWNWARD)
                    camera_dir = Tello.CAMERA_DOWNWARD
                else:
                    tello.set_video_direction(Tello.CAMERA_FORWARD)
                    camera_dir = Tello.CAMERA_FORWARD
                time.sleep(0.5)     # 映像が切り替わるまで待つ

            # 10秒おきに'command'を送って死活チェックする
            current_time = time.time()
            if current_time - pre_time > 10.0:
                tello.send_command_without_return('command')
                pre_time = current_time

    # Ctrl+Cが押されたらループ離脱
    except(KeyboardInterrupt, SystemExit):
        print('Ctrl+C を検知')

    ###########
    # 終了処理
    ###########
    cv2.destroyAllWindows()
    tello.set_video_direction(Tello.CAMERA_FORWARD)
    tello.streamoff()
    frame_read.stop()
    del tello.background_frame_read
    del tello

if __name__ == "__main__":
    main()