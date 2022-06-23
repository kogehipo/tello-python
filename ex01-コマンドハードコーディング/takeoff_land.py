#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Telloを四角形の軌跡で自動飛行させる
# これは下記ページを元にしている
# https://deviceplus.jp/hi-tech/drone-on-auto-pilot-with-python-03/
 
import socket
import time

#Create a UDP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1' , 8889)

# コマンドモードに設定
socket.sendto('command'.encode('utf-8'), tello_address)

# 離陸
socket.sendto('takeoff'.encode('utf-8'), tello_address)
print('takeoff')
time.sleep(3)

# 前進
socket.sendto('forward 50'.encode('utf-8'), tello_address)
print('forward')
time.sleep(3)

# 左移動
socket.sendto('left 100'.encode('utf-8'), tello_address)
print('left')
time.sleep(3)

# 後退
socket.sendto(' back 100'.encode('utf-8'), tello_address)
print('back')
time.sleep(3)

# 右移動
socket.sendto('right 100'.encode('utf-8'), tello_address)
print('right')
time.sleep(3)

# 左へ90度旋回
socket.sendto('ccw 90'.encode('utf-8'), tello_address)
print('ccw')
time.sleep(3)

# 右へ90度旋回
socket.sendto('cw 90'.encode('utf-8'), tello_address)
print('cw')
time.sleep(3)

# フリップ
socket.sendto('flip r'.encode('utf-8'), tello_address)   # 右へフリップ
print('flip')
time.sleep(3)

# 着陸
socket.sendto('land'.encode('utf-8'), tello_address)
print('land')

