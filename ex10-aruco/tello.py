#!/usr/bin/env python
import cv2
import os
import numpy as np 
import socket
import time
import threading
# import keyboard
from PIL import Image
import sys
from cv2 import aruco

class ArucoDetect:
    def __init__(self) -> None:
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters()

    def detect(self, frame):
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            frame, self.aruco_dict, parameters=self.parameters)
        return corners, ids  # , rejectedImgPoints

aruco_detector = ArucoDetect()

# VideoCapture用のオブジェクト準備
cap = None
# データ受信用のオブジェクト準備
response = None

cv2.namedWindow("Detect Points", cv2.WINDOW_AUTOSIZE)
cv2.moveWindow("Detect Points", 100, 100)
img = np.zeros((480,640,3), np.uint8) # y座標, x座標, チャンネル
img[:,:] = [255, 255, 255] 

#Create a UDP socket
socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1' , 8889)
#command-mode : 'command'
socket1.sendto('command'.encode('utf-8'),tello_address)
print ('start')
socket1.sendto('streamon'.encode(),tello_address)

state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#state_address =('0.0.0.0',8890)
state_sock.bind(("", 8890))
data, _= state_sock.recvfrom(1024)
print(data)

        # 状態を受信して表示

#state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#state_sock.bind(("", 8890))
#data, _ = socket1.recvfrom(1024)
#print()
print("Tello Python3 Demo.")
#print(data.decode())

def run_udp_receiver():
    while True:
        try:
            response, _ = socket1.recvfrom(1024)
        except Exception as e:
            print(e)
            break

thread = threading.Thread(target=run_udp_receiver, args=())
thread.daemon = True
thread.start()


"""
def receive_video():
    global img
    # OpenCV を用いて UDP 11111番ポートで動画を待ち受ける
    cap = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1")

    while True:
        # 動画の1フレーム (1枚分の画像) を取得する
        success, image = cap.read()
        if not success:
            continue
#        print('success')
        # OpenCVの画像形式(BGR)をRGBに変換する
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 画像を img に設定する
#        img.set_image(imageRGB)
        img=cv2.resize(imageRGB,(640,480))

video_receive_thread = threading.Thread(target=receive_video)
video_receive_thread.start()
"""

#x = input('ドローンの進む距離を入力してください(cm単位): ')
x=20
y1 = 'forward '+str(x)
y2 = 'left '+str(x)
y3 = 'back '+str(x)
y4 = 'right '+str(x)
y7 = 'move_up '+str(x)

#z = input('旋回する角度を決めてください(度): ')
z=4
y5 = 'ccw '+str(z)
y6 = 'cw '+str(z)
#
n = 0
#
def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)
b = 0

while True:
    cv2.imshow("Detect Points", img)
    key = cv2.waitKey(1) #& 0xff
    socket1.sendto('streamon'.encode('utf-8'), tello_address)
    vaddress = 'udp://@0.0.0.0:11111'
    if cap is None:
        cap = cv2.VideoCapture(vaddress)
    if not cap.isOpened():
        cap.open(vaddress)
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    corners, ids = aruco_detector.detect(frame)
    if ids is not None:
#        print('-----')
#        print(len(ids))
#        print(len(corners))
#        print('-----')
        
        
        for i in range(len(ids)):
            print("ids",ids[i][0])
            pt1 = corners[i][0][0]

            we1= corners[i][0][0]
            we2= corners[i][0][1]
            we3= corners[i][0][2]
            we4= corners[i][0][3]

            le11=int(we1[0])
            le12=int(we1[1])
            le21=int(we2[0])
            le22=int(we2[1])
            le31=int(we3[0])
            le32=int(we3[1])
            le41=int(we4[0])
            le42=int(we4[1])
            centerx=int((we1[0] + we2[0] + we3[0] + we4[0])/4)    
            centery=int((we1[1] + we2[1] + we3[1] + we4[1])/4)
            print(centerx,centery)
 #           print(le12,le42)
        #図形の座標見本    

           # print(we1,we1[0],we1[1])
            #print(we2,we2[0],we2[1])
            #print(we3,we3[0],we3[1])
            #print(we4,we4[0],we4[1])
            cv2.circle(img,center=(le11,le12),radius=5,color=(255,0,0),thickness=2)#左下
            cv2.circle(img,center=(le21,le22),radius=5,color=(0,255,0),thickness=2)#左上
            cv2.circle(img,center=(le31,le32),radius=5,color=(0, 0,255),thickness=2)#右上
            cv2.circle(img,center=(le41,le42),radius=5,color=(85,85,85),thickness=2)#右下
            cv2.circle(img,center=(centerx,centery),radius=10,color=(0, 255, 0),thickness=4)
            #print("corners",corners[i][0][0][0])
           #print("corners",corners[i][0][1][0]) 
            #print("corners",corners[i][0][2][0]) 
            #print("corners",corners[i][0][3][0])  
           #print("corners",corners[i][0][0][1])

           # for j  in range(4)
           #中心座標（128,50)
           
        #if centerx > 260:
            #img[:,:] = [255, 255, 255]
            #socket.sendto(y2.encode('utf-8'),tello_address) #機体が前を向いたまま左に横移動
            #print("左移動")

        #if centerx < 250:
            #img[:,:] = [255, 255, 255]
            #socket.sendto(y4.encode('utf-8'),tello_address) #機体が前を向いたまま右に横移動
            #print("右移動")

        #if centery > 55:
            #img[:,:] = [255, 255, 255]
            #print(y1) #デバック
            #socket.sendto(y1.encode('utf-8'),tello_address) #機体が前進する
            #print("前進")

        #if centery >45:
            #img[:,:] = [255, 255, 255]
            #socket.sendto(y3.encode('utf-8'),tello_address) #機体が前を向いたまま後進
            #print("後退")


#左上からブルー　グリーン　レッド　灰色

    if key == -1:
        pass
        # print("")
    elif key == ord("z"):
        img[:,:] = [255, 255, 255]
        socket1.sendto('takeoff'.encode('utf-8'),tello_address) #機体が離陸する
        print("離陸")

    elif key == ord("w"):
        img[:,:] = [255, 255, 255]
        print(y1) #デバック
        socket1.sendto(y1.encode('utf-8'),tello_address) #機体が前進する
        print("前進") 

    elif key == ord("v"):
        img[:,:] = [255, 255, 255]
        print(y5) #デバック
        socket1.sendto(y5.encode('utf-8'),tello_address) #機体が前進する
        print("左回転") 

    elif key == ord("b"):
        img[:,:] = [255, 255, 255]
        print(y6) #デバック
        socket1.sendto(y6.encode('utf-8'),tello_address) #機体が前進する
        print("右回転") 

    elif key == ord("a"):
        
        socket1.sendto(y2.encode('utf-8'),tello_address) #機体が前を向いたまま左に横移動
        print("左移動")
        
    elif key == ord("s"):
        img[:,:] = [255, 255, 255]
        socket1.sendto(y3.encode('utf-8'),tello_address) #機体が前を向いたまま後進
        print("後退")
        
    elif key == ord("d"):
        img[:,:] = [255, 255, 255]
        socket1.sendto(y4.encode('utf-8'),tello_address) #機体が前を向いたまま右に横移動
        print("右移動")

    elif key == ord("c"):
        img[:,:] = [255, 255, 255]
        socket1.sendto('downvision 1'.encode('utf-8'),tello_address) #機体が前を向いたまま右に横移動
        print("切り替え")
    
    elif key == ord("C"):
        img[:,:] = [255, 255, 255]
        socket1.sendto('downvision 0'.encode('utf-8'),tello_address) #機体が前を向いたまま右に横移動
        print("メインカメラ")

    elif key == ord('f'):
        cv2.imwrite('frame1.jpg',frame)
        print("写真")
   
    elif key == ord('u'):#自動追跡モード
            print('解除したい場合mキーを押して下さい')
            time.sleep(1)
            xl=150-10
            xh=150+10
            yl=100-10
            yh=100+10

            while True:
                
                cv2.imshow("Detect Points", img)
                key = cv2.waitKey(1) #& 0xff
                socket1.sendto('streamon'.encode('utf-8'), tello_address)
                vaddress = 'udp://@0.0.0.0:11111'
                if cap is None:
                    cap = cv2.VideoCapture(vaddress)
                if not cap.isOpened():
                    cap.open(vaddress)
                ret, frame = cap.read()
                cv2.imshow('frame', frame)

                corners, ids = aruco_detector.detect(frame)
                if ids is not None:
                    print('-----')
#                    print(len(ids))
#                    print(len(corners))
#                    print('-----')
                    we1= corners[i][0][0]
                    we2= corners[i][0][1]
                    we3= corners[i][0][2]
                    we4= corners[i][0][3]

                    le11=int(we1[0])
                    le12=int(we1[1])
                    le21=int(we2[0])
                    le22=int(we2[1])
                    le31=int(we3[0])
                    le32=int(we3[1])
                    le41=int(we4[0])
                    le42=int(we4[1])
                    centerx=int((we1[0] + we2[0] + we3[0] + we4[0])/4)    
                    centery=int((we1[1] + we2[1] + we3[1] + we4[1])/4)
 #                   if key ==('p'):
                    print(centerx,centery)

# 機体は画像上では機首を左向きに飛行していることとする
#
#      *       左
#    (AR)
#
#
                if ids is not None:
                    img[:,:] = [255, 255, 255]
                    if centerx > xh:
                        socket1.sendto('back 20'.encode('utf-8'),tello_address) #機体が前を向いたまま左に横移動
                        print('機体後進：ARマーカは左移動')

                    if centerx < xl:
#                        img[:,:] = [255, 255, 255]
                        socket1.sendto('forward 20'.encode('utf-8'),tello_address) #機体が前を向いたまま右に横移動
                        print('機体前進：ARマーカは右移動')

                    if centery > yh:
#                        img[:,:] = [255, 255, 255]
                        socket1.sendto('left 20'.encode('utf-8'),tello_address) #機体が前進する
                        print('機体左移動：ARマーカは上移動')

                    if centery < yl:
#                        img[:,:] = [255, 255, 255]
                        socket1.sendto('right 20'.encode('utf-8'),tello_address) #機体が前を向いたまま後進
                        print('機体右移動：ARマーカは下移動')

                if yl < centery <yh or xl< centerx < xh :
                    socket1.sendto('stop'.encode('utf-8'),tello_address)
                    print('stop')

                if yl < centery <yh and xl< centerx < xh :
#                        socket1.sendto('stop'.encode('utf-8'),tello_address)
                    print('GOAL')
                    socket1.sendto('land'.encode('utf-8'),tello_address)  #機体が着陸
                    print("着陸")
                    break

                if key == ord('m'):
                    print('解除')
                    break
            time.sleep(1)

    elif key ==ord("k"):#向きを整える
        print('向きを整えます 解除したい場合mキーを押して下さい')
        while True:
            
            cv2.imshow("Detect Points", img)
            key = cv2.waitKey(1) #& 0xff
            socket1.sendto('streamon'.encode('utf-8'), tello_address)
            vaddress = 'udp://@0.0.0.0:11111'
            if cap is None:
                cap = cv2.VideoCapture(vaddress)
            if not cap.isOpened():
                cap.open(vaddress)
            ret, frame = cap.read()
            cv2.imshow('frame', frame)

            corners, ids = aruco_detector.detect(frame)
            if ids is not None:
                for i in range(len(ids)):
                    print("ids",ids[i][0])
                    pt1 = corners[i][0][0]

                    we1= corners[i][0][0]
                    we2= corners[i][0][1]
                    we3= corners[i][0][2]
                    we4= corners[i][0][3]

                    le11=int(we1[0])
                    le12=int(we1[1])
                    le21=int(we2[0])
                    le22=int(we2[1])
                    le31=int(we3[0])
                    le32=int(we3[1])
                    le41=int(we4[0])
                    le42=int(we4[1])
                    centerx=int((we1[0] + we2[0] + we3[0] + we4[0])/4)    
                    centery=int((we1[1] + we2[1] + we3[1] + we4[1])/4)
                    
                    print(centerx,centery)
                    print(le12,le42)

            if key == ord('m'):
                print('解除')
                break
            if ids is not None:
                abss=abs(le12-le42)
                print("abs=",abss)
                if abs(le12-le42)<12:
                    socket1.sendto('stop'.encode('utf-8'),tello_address)
                    continue
                if le12 >le42:
                    img[:,:] = [255, 255, 255]
                    socket1.sendto('cw 4'.encode('utf-8'),tello_address)
                    print('右回転')
                    continue
                if le42 >le12:
                    img[:,:] = [255, 255, 255]
                    socket1.sendto('ccw 4'.encode('utf-8'),tello_address)
                    print('左回転')
                    continue

    elif key ==ord("h"):#降下
        img[:,:] = [255, 255, 255]
        print('現在の高さを出します')#tofが高さ
        data, _= state_sock.recvfrom(1024)
        print(data)
        height1= input('降下する高さを決めてください(cm): ')
        h1 = 'down '+str(height1)
        socket1.sendto(h1.encode('utf-8'),tello_address)

    elif key ==ord("t"):#上昇
        img[:,:] = [255, 255, 255]
        data, _= state_sock.recvfrom(1024)
        print(data)
        socket1.sendto('up 20'.encode('utf-8'),tello_address)
        print("上昇")

    elif key == ord("l"):
        img[:,:] = [255, 255, 255]
        socket1.sendto('land'.encode('utf-8'),tello_address)  #機体が着陸
        print("着陸")

    elif key == ord("q"):
        img[:,:] = [255, 255, 255]
        socket1.sendto('land'.encode('utf-8'),tello_address)  #機体が着陸
        print("着陸 終了")
        break
        
cap.release()
cv2.destroyAllWindows()

socket1.sendto('streamoff'.encode('utf-8'), tello_address)