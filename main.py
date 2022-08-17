# https://imagingsolution.net/program/python/tkinter/display_opencv_video_canvas/

import pickle
import tkinter as tk
from tkinter import messagebox
#import stapipy as st
import cv2 as cv
from PIL import Image, ImageTk # Pillow
import stapipy as st
import camera
import judge
#import node_value_change
#import mouse_event
from multiprocessing import Process, Queue, pool
import time
import numpy as np
from datetime import datetime
import trigger
import dill
import pickle
import image_convert
import signal
import threading
import gc
import tkinter as tk
import pyautogui  # 外部ライブラリ
from PIL import Image, ImageTk  # 外部ライブラリ
from PySide6.QtWidgets import *
from PySide6.QtCore import *


# Image scale when displaying using OpenCV.
DISPLAY_RESIZE_FACTOR = 0.3
# imposible to set infinity as -1
i = 999999999999999
PIXEL_FORMAT = "UserOutputValue0"
RESIZE_RETIO = 2 # 縮小倍率の規定
canvas_width = 500
canvas_height = 310


def main(q, r):
    # camera initialization
    st.initialize()
    st_system = st.create_system()
    st_device = st_system.create_first_device()
    st_datastream = st_device.create_datastream()
    st_datastream.start_acquisition(i)
    st_device.acquisition_start()
    remote_nodemap = st_device.remote_port.nodemap # impossible to pick it, so combined into the main program

    while st_datastream.is_grabbing: # A while loop for acquiring data and checking status
        data = camera.loop(st_datastream) # data from the camera.py
        q.put(data) # for image
        sim_fact = judge.judgement(data) # template matching and similarity factor
        if sim_fact > 0.9:
            ok = "OK"
            r.put(ok) # for image

        else: #
            ng = "NG"
            r.put(ng) # for image
            trigger.edit_enumeration(remote_nodemap, PIXEL_FORMAT, 1)
            # メッセージボックス（情報）
            #tk.messagebox.showinfo('確認', 'もうすぐ誕生日です')
            trigger.edit_enumeration(remote_nodemap, PIXEL_FORMAT, 0)
            print("NG")

    # convert the image from nupy to image for the TK
def converter(q, s):
    while True:
        image_tk = image_convert.converter(q.get())
        s.put(image_tk)

def save(q):
    while True:
        cv.imwrite('D:\\Programing\\PycharmProjects\\image_processing\\data\\a.jpg', q.get(), [cv.IMWRITE_JPEG_QUALITY, 100])

class Mainloop(tk.Frame):
    def __init__(self, r, master=None):
        super().__init__(master)
        self.pack()

        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)

        button = tk.Button(text='ボタン', width=30, command=self.thread)
        button.place(x=5, y=400)
        button.bind('<Button-1>', )

        #フレームを入れ子で作成。「frame」の中に「canvas」を作成
        frame = tk.Frame(root, relief=tk.FLAT)
        frame.place(x=5, y=5, width=canvas_width, height=canvas_height)
        ### キャンバス作成・配置
        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        self.canvas.place(x=5, y=5)
        self.canvas1 = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        self.canvas1.place(x=530, y=5)

        self.text= tk.StringVar()
        self.text.set("aaaa")
        self.text_pos = tk.Label(root, textvariable=self.text)
        self.text_pos.place(x=5, y=5)

    #@pyqtSlot(str)
    def canvas_update(self, r, s):
        increment_OK = 0
        increment_NG = 0

        # Canvasウィジェットを配置し、各種イベントを設定
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-1>", self.start_point_get)
        self.canvas.bind("<Button1-Motion>", self.rect_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.release_action)

        print(self.start_x, self.start_y, self.end_x, self.end_y)
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='white')

        self.image_tk = ImageTk.PhotoImage(s.get())
        # 画像の描画
        self.canvas.create_image(
            #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
            #self.canvas_height / 2,
            0, 0, image=self.image_tk, anchor='nw')

        if r.get() == "OK":
            increment_OK += 1
            self.text.set("OK" + " " + str(increment_OK))
        else:
            increment_NG += 1
            self.text.set("NG" + " " + str(increment_NG))

    # ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
    def start_point_get(self, event):
        global start_x, start_y # グローバル変数に書き込みを行なうため宣言

        self.canvas.delete("rect1")  # すでに"rect1"タグの図形があれば削除

        # canvas上に四角形を描画（rectangleは矩形の意味）
        self.canvas.create_rectangle(event.x,
                                 event.y,
                                 event.x + 1,
                                 event.y + 1,
                                 outline="white",
                                 tag="rect1")
        # グローバル変数に座標を格納
        start_x, start_y = event.x, event.y

    # ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
    def rect_drawing(self, event):

        # ドラッグ中のマウスポインタが領域外に出た時の処理
        if event.x < 0:
            end_x = 0
        else:
            end_x = min(canvas_width, event.x)
        if event.y < 0:
            end_y = 0
        else:
            end_y = min(canvas_height, event.y)

        # "rect1"タグの画像を再描画
        self.canvas.coords("rect1", start_x, start_y, end_x, end_y)

    # ドラッグを離したときのイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
    def release_action(self, event):

        # "rect1"タグの画像の座標を元の縮尺に戻して取得
        self.start_x, self.start_y, self.end_x, self.end_y = [
            round(n * RESIZE_RETIO) for n in self.canvas.coords("rect1")
        ]

        # 取得した座標の部分を切り出し
        coordination = pyautogui.confirm(text="検索範囲に指定しますか?", title="検索範囲", buttons=["Yes","No"])

        if coordination == "Yes":

            # 画像の描画
            im = Image.open('D:\\Programing\\PycharmProjects\\image_processing\\data\\a.jpg')
            im_crop = im.crop((self.start_x, self.start_y, self.end_x, self.end_y))
            im_crop.save('D:\\Programing\\PycharmProjects\\image_processing\\data\\b.jpg', quality=100)

            image_tk = image_convert.converter(im_crop)
            image_tk = ImageTk.PhotoImage(image_tk)
            self.canvas1.create_image(
                #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                #self.canvas_height / 2,
                0, 0, image=image_tk)



        else:
            self.canvas.delete("rect1")  # すでに"rect1"タグの図形があれば削除
            pass

    def thread(self):
        thread = threading.Thread(target=self.canvas_update, args=(r, s, ))
        thread.start()


if __name__ == "__main__":

    q = Queue()
    r = Queue()
    s = Queue()

    with pool.Pool(processes=3) as p:

        #multiprocessing
        p0 = p.Process(target=main, args=(q, r, ), daemon=True)
        p1 = p.Process(target=converter, args=(q, s, ), daemon=True)
        p2 = p.Process(target=save, args=(q, ), daemon=True)

        p0.start()
        p1.start()
        p2.start()

    root = tk.Tk()
    root.title("Hello World")
    root.geometry("1024x768")
    app = Mainloop(r, master = root)
    app.mainloop()

