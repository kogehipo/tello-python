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
#
# 水平ライントレースに加えて、垂直ライントレースの機能を追加中。
# auto_mode で自動モードを制御。

from djitellopy import Tello    # DJITelloPyのTelloクラスをインポート
import time                     # time.sleepを使いたいので
import cv2                      # OpenCVを使うため
import numpy as np              # ラベリングにNumPyが必要なので

# メイン関数
def main():

    ###########
    # 初期化
    ###########
    # Telloクラスを使って，telloというインスタンスを作る
    tello = Tello(retry_count=1)    # 応答が来ないときのリトライ回数は1(デフォルトは3)
    tello.RESPONSE_TIMEOUT = 0.01   # コマンド応答のタイムアウトは短くした(デフォルトは7)

    # Telloへ接続
    tello.connect()
    #tello.connect(False)  # Windows/WSL対応のためFalseを追加（ex05を参照）

    # 画像転送を有効にする
    tello.streamoff()   # 誤動作防止の為、最初にOFFする
    tello.streamon()    # 画像転送をONに

    # BackgrounfFrameReadクラスのインスタンスを通して画像フレームを取得する
    frame_read = tello.get_frame_read()     # インスタンスを作る

    current_time = time.time()  # 現在時刻
    pre_time = current_time     # 前回、死活チェックを行った時刻

    # SDKバージョンを問い合わせ
    sdk_ver = tello.query_sdk_version()

    # モータとカメラの切替フラグ
    motor_on = False                    # モータON/OFFのフラグ
    camera_dir = Tello.CAMERA_FORWARD   # 前方/下方カメラの方向のフラグ

    # 前回強制終了して下方カメラかもしれないので
    if sdk_ver == '30':                                     # SDK 3.0に対応しているか？ 
        tello.set_video_direction(Tello.CAMERA_FORWARD)     # カメラは前方に

    # トラックバーを作るため，まず最初にウィンドウを生成
    cv2.namedWindow("OpenCV Window")

    # トラックバーのコールバック関数は何もしない空の関数
    def nothing(x):
        pass    # passは何もしないという命令

    # トラックバーの生成
    cv2.createTrackbar("H_min", "OpenCV Window", 0, 179, nothing)       # Hueの最大値は179
    cv2.createTrackbar("H_max", "OpenCV Window", 179, 179, nothing)
    cv2.createTrackbar("S_min", "OpenCV Window", 0, 255, nothing)
    cv2.createTrackbar("S_max", "OpenCV Window", 255, 255, nothing)
    cv2.createTrackbar("V_min", "OpenCV Window", 0, 255, nothing)
    cv2.createTrackbar("V_max", "OpenCV Window", 255, 255, nothing)
    
    # 自動モードフラグ
    # 0: 手動操縦
    # 1: 対象の色をトラックバーで設定して、水平ライントレース
    # 2: 固定の色設定で水平ライントレース（Macbookでトラックバーが動作しないので）
    # 3: 固定の色設定で垂直ライントレース
    auto_mode = 0
    direction = 0
    default_speed = 30  # トレースするときの初速度

    time.sleep(0.5)     # 通信安定するまで待つ

    print('Tello is starting...')

    ###########
    # ループ
    ###########
    try:
        # 永久ループで繰り返す
        while True:

            # (1) 画像取得
            image = frame_read.frame    # 映像を1フレーム取得しimage変数に格納

            # (2) 画像サイズ変更と、カメラ方向による回転
            small_image = cv2.resize(image, dsize=(480,360) )   # 画像サイズを半分に縮小

            # 下向きカメラは90°回転して画像の上を前方にする
            if camera_dir == Tello.CAMERA_DOWNWARD:
                small_image = cv2.rotate(small_image, cv2.ROTATE_90_CLOCKWISE)

            # (3) ここから画像処理
            if auto_mode == 1 or auto_mode == 2:
                # 水平ライントレースの場合は注目する領域（下半分）を切り取る
                bgr_image = small_image[250:359,0:479]
            else:
                bgr_image = small_image

            hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)  # BGR画像 -> HSV画像

            # (4) 追跡する対象物の色範囲を設定
            if auto_mode == 1:
                # トラックバーを使う場合はその値を取得
                h_min = cv2.getTrackbarPos("H_min", "OpenCV Window")
                h_max = cv2.getTrackbarPos("H_max", "OpenCV Window")
                s_min = cv2.getTrackbarPos("S_min", "OpenCV Window")
                s_max = cv2.getTrackbarPos("S_max", "OpenCV Window")
                v_min = cv2.getTrackbarPos("V_min", "OpenCV Window")
                v_max = cv2.getTrackbarPos("V_max", "OpenCV Window")
            elif auto_mode == 2 or auto_mode == 3:
                # モード２,3の場合は固定の色設定を使う。Macbookでトラックバーが動作しないため。
                # また、Jetsonでは画面サイズが小さく操作できないため。
                '''
                # ケーブルドラムの緑色
                # 黄
                #h_min = 10
                #h_max = 60
                # 緑
                h_min = 30
                h_max = 90
                # 青
                #h_min = 90
                #h_max = 150
                s_min = 64
                s_max = 255
                v_min = 0
                v_max = 255
                '''
                # 黒色
                h_min = 0
                h_max = 179
                s_min = 0
                s_max = 255
                v_min = 0
                v_max = 60

            # (5) 対象物をトレースさせる処理
            if auto_mode == 1 or auto_mode == 2 or auto_mode == 3:
                # inRange関数で範囲を指定して、HSV画像を２値化。HSV画像なのでタプルもHSV並びで指定。
                bin_image = cv2.inRange(hsv_image, (h_min, s_min, v_min), (h_max, s_max, v_max))

                # ２値画像を15×15に膨張させて虎ロープの画像をつなげる
                # 虎ロープではない場合も有効と思われる。
                kernel = np.ones((15,15), np.uint8)
                bin_image = cv2.dilate(bin_image, kernel, iterations=1)

                # 元のHSV画像に２値画像でマスクをかける -> マスクされた部分の色だけ残る
                # （HSV画像 AND HSV画像 なので，自分自身とのANDは何も変化しない->マスクだけ効かせる）
                result_image = cv2.bitwise_and(hsv_image, hsv_image, mask=bin_image)

                if auto_mode == 3:    # 垂直トレースの場合は対象画像を進行方向に回転する
                    # 座標の変換 (回転の中心、回転角度、拡大率)
                    rotMat = cv2.getRotationMatrix2D((240,180), direction, 1)
                    # 画像を回転　(入力画像の配列、変換行列、出力画像サイズ)
                    result_image = cv2.warpAffine(result_image, rotMat, (480,360))
                    bin_image = cv2.warpAffine(bin_image, rotMat, (480,360))

                # 面積・重心計算付きのラベリング処理を行う
                num_labels, label_image, stats, center = cv2.connectedComponentsWithStats(bin_image)

                # 最大のラベルは画面全体を覆う黒なので不要．データを削除
                num_labels = num_labels - 1
                stats = np.delete(stats, 0, 0)
                center = np.delete(center, 0, 0)

                if num_labels >= 1:
                    # 面積最大のインデックスを取得
                    max_index = np.argmax(stats[:,4])
                    #print(max_index)

                    # 面積最大のラベルのx,y,w,h,面積s,重心位置mx,myを得る
                    x = stats[max_index][0]
                    y = stats[max_index][1]
                    w = stats[max_index][2]
                    h = stats[max_index][3]
                    s = stats[max_index][4]
                    mx = int(center[max_index][0])
                    my = int(center[max_index][1])
                    #print("(x,y)=%d,%d (w,h)=%d,%d s=%d (mx,my)=%d,%d"%(x, y, w, h, s, mx, my) )

                    # ラベルを囲うバウンディングボックスを描画
                    cv2.rectangle(result_image, (x, y), (x+w, y+h), (255, 0, 255))

                    # 重心位置の座標と面積を表示
                    cv2.putText(result_image, "%d,%d"%(mx,my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
                    cv2.putText(result_image, "%d"%(s), (x, y+h+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))

                    # 自動操縦のときは、ここで飛行方向を決める
                    if auto_mode == 1 or auto_mode == 2:   # 水平トレース
                        speed = default_speed  # 前方への進行速度は一定

                        # 制御式(0.4はゲイン、様子を見て調整すること)
                        dx = 0.4 * (240 - mx)       # 画面横幅480について、画面中心との差分

                        # 旋回方向の不感帯を設定（±20未満ならゼロにする）
                        d = 0.0 if abs(dx) < 10.0 else dx

                        # 旋回方向のソフトウェアリミッタ(±100を超えないように)
                        d =  100 if d >  100.0 else d
                        d = -100 if d < -100.0 else d

                        d = -d  # 旋回方向が逆だったので符号を反転

                        print('dx=%f'%(dx) )
                        # 引数の意味： left-right velocity, forward-backward, up-down, yaw
                        tello.send_rc_control( 0, int(speed), 0, int(d) )

                    elif auto_mode == 3:    # 垂直トレース
                        speed = default_speed  # 前方への進行速度は一定

                        # 制御式(0.4はゲイン、様子を見て調整すること)
                        dx = 0.4 * (240 - mx)       # 画面横幅480について、画面中心との差分

                        # 旋回方向の不感帯を設定（±20未満ならゼロにする）
                        d = 0.0 if abs(dx) < 10.0 else dx

                        # 旋回方向のソフトウェアリミッタ(±100を超えないように)
                        d =  100 if d >  100.0 else d
                        d = -100 if d < -100.0 else d

                        d = -d  # 旋回方向が逆だったので符号を反転

                        direction += d  # 飛行方向を調整
                        print('direction=%f'%(direction) )
                        x = np.sin(np.radians(direction)) * speed
                        z = np.cos(np.radians(direction)) * speed * 1.5   # 上下方向は鈍いので+50%のゲタを履かせる
                        #drone.send_command('rc %s %s %s %s'%(int(a), int(b), int(c), int(d)) )
                            # 引数の意味： left-right velocity, forward-backward, up-down, yaw
                        tello.send_rc_control( int(x), 0, int(z), 0 )

                    '''
                    elif auto_mode == 3:    # 垂直トレース
                        a = b = c = d = 0

                        # up down制御式(ゲインは低めの0.3)
                        cx = 0.3 * (180 - my)       # 画面tate幅360について、画面中心との差分

                        # up down方向の不感帯を設定（±20未満ならゼロにする）
                        c = 0.0 if abs(cx) < 10.0 else cx

                        # up down方向のソフトウェアリミッタ(±100を超えないように)
                        c =  100 if c >  100.0 else c
                        c = -100 if c < -100.0 else c

                        c = -c  # up down方向が逆だったので符号を反転

                        print('cx=%f'%(cx) )
                        #drone.send_command('rc %s %s %s %s'%(int(a), int(b), int(c), int(d)) )
                            # 引数の意味： left-right velocity, forward-backward, up-down, yaw
                        #tello.send_rc_control( int(a), int(b), int(c), int(d) )


                        # slide制御式(ゲインは低めの0.3)
                        ax = 0.1 * (240 - mx)       # 画面横幅480について、画面中心との差分

                        # slide方向の不感帯を設定（±20未満ならゼロにする）
                        a = 0.0 if abs(ax) < 10.0 else ax

                        # slide方向のソフトウェアリミッタ(±100を超えないように)
                        a =  100 if a >  100.0 else a
                        a = -100 if a < -100.0 else a

                        a = -a  # slide方向が逆だったので符号を反転

                        print('ax=%f'%(ax) )
                        #drone.send_command('rc %s %s %s %s'%(int(a), int(b), int(c), int(d)) )
                            # 引数の意味： left-right velocity, forward-backward, up-down, yaw
                        tello.send_rc_control( int(a), int(b), int(c), int(d) )
                    '''

            # 円周運動をさせる
            elif auto_mode == 4:
                # 速度speedで、方向direction(上方向0度〜時計回りに359度)へ移動させる。
                # ここでは360ステップで1回転させている。
                speed = default_speed
                direction += 1
                if 360 <= direction:
                    direction = 0
                x = np.sin(np.radians(direction)) * speed
                z = np.cos(np.radians(direction)) * speed * 1.5   # 上下方向は鈍いので+50%のゲタを履かせる
                print("x=",x," z=",z)
                # 引数の意味： left-right, forward-backward, up-down, yaw
                tello.send_rc_control( int(x), 0, int(z), 0 )


            # (6) ウィンドウに画像を表示
            #cv2.imshow("OpenCV Window", small_image)
            cv2.imshow('OpenCV Window', result_image)    # ウィンドウに表示するイメージを変えれば色々表示できる
            cv2.imshow('Binary Image', bin_image) 

            # (7) OpenCVウィンドウでキー入力を1ms待つ
            # このコマンドはOpenCVのウインドウでタイプすること。
            key = cv2.waitKey(1) & 0xFF

            if key == 27:                   # key が27(ESC)だったらwhileループを脱出，プログラム終了
                break
            elif key == ord('t'):           # 離陸
                tello.takeoff()
            elif key == ord('l'):           # 着陸
                tello.send_rc_control( 0, 0, 0, 0 )
                tello.land()
            elif key == ord('w'):           # 前進 30cm
                tello.move_forward(30)
            elif key == ord('s'):           # 後進 30cm
                tello.move_back(30)
            elif key == ord('a'):           # 左移動 30cm
                tello.move_left(30)
            elif key == ord('d'):           # 右移動 30cm
                tello.move_right(30)
            elif key == ord('e'):           # 旋回-時計回り 30度
                tello.rotate_clockwise(30)
            elif key == ord('q'):           # 旋回-反時計回り 30度
                tello.rotate_counter_clockwise(30)
            elif key == ord('r'):           # 上昇 30cm
                tello.move_up(30)
            elif key == ord('f'):           # 下降 30cm
                tello.move_down(30)
            elif key == ord('p'):           # ステータスをprintする
                print(tello.get_current_state())
            elif key == ord('m'):           # モータ始動/停止を切り替え
                if sdk_ver == '30':         # SDK 3.0に対応しているか？
                    if motor_on == False:       # 停止中なら始動 
                        tello.turn_motor_on()
                        motor_on = True
                    else:                       # 回転中なら停止
                        tello.turn_motor_off()
                        motor_on = False
            elif key == ord('c'):           # カメラの前方/下方の切り替え
                if sdk_ver == '30':         # SDK 3.0に対応しているか？
                    if camera_dir == Tello.CAMERA_FORWARD:     # 前方なら下方へ変更
                        tello.set_video_direction(Tello.CAMERA_DOWNWARD)
                        camera_dir = Tello.CAMERA_DOWNWARD     # フラグ変更
                    else:                                      # 下方なら前方へ変更
                        tello.set_video_direction(Tello.CAMERA_FORWARD)
                        camera_dir = Tello.CAMERA_FORWARD      # フラグ変更
                    time.sleep(0.5)     # 映像が切り替わるまで少し待つ
            elif key == ord('1'):       # 水平ライントレースON（トラックバー使用する）
                auto_mode = 1
            elif key == ord('2'):       # 水平ライントレースON（トラックバー使用しない）
                auto_mode = 2
            elif key == ord('3'):       # 垂直ライントレースON（トラックバー使用しない）
                auto_mode = 3
                direction = 45          # 移動方向の初期値は右上
            elif key == ord('4'):       # 垂直に円を描く
                auto_mode = 4
                direction = 90          # 移動方向の初期値は右
            elif key == ord('0'):       # 追跡モードOFF
                tello.send_rc_control( 0, 0, 0, 0 )
                auto_mode = 0
                direction = 0


            # (8) 10秒おきに'command'を送って、死活チェックを通す
            current_time = time.time()                          # 現在時刻を取得
            if current_time - pre_time > 10.0 :                 # 前回時刻から10秒以上経過しているか？
                tello.send_command_without_return('command')    # 'command'送信
                pre_time = current_time                         # 前回時刻を更新

    # Ctrl+Cが押されたらループ離脱
    except( KeyboardInterrupt, SystemExit):
        print( "Ctrl+c を検知" )

    ###########
    # 終了処理
    ###########
    cv2.destroyAllWindows()                             # すべてのOpenCVウィンドウを消去
    
    if sdk_ver == '30':                                 # SDK 3.0に対応しているか？
        tello.set_video_direction(Tello.CAMERA_FORWARD) # カメラは前方に戻しておく

    tello.streamoff()                                   # 画像転送を終了(熱暴走防止)
    frame_read.stop()                                   # 画像受信スレッドを止める

    del tello.background_frame_read                     # フレーム受信のインスタンスを削除    
    del tello                                           # telloインスタンスを削除

# "python3 XXXX.py"として実行された時だけ動く様にするおまじない処理
# importされると__name_に"__main__"は入らないので，pyファイルが実行されたのかimportされたのかを判断できる．
if __name__ == "__main__":
    main()    # メイン関数を実行
