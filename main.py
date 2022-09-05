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
from PIL import Image
from tkinter import messagebox
import test

# Image scale when displaying using OpenCV.
DISPLAY_RESIZE_FACTOR = 1
# imposible to set infinity as -1
i = 999999999999999
PIXEL_FORMAT = "UserOutputValue0"
RESIZE_RETIO = 1 # 縮小倍率の規定
canvas_width = 500
canvas_height = 310

############ qでカメラからの読み取りを失敗したときの処理から

def main(q, r):
    # camera initialization
    st.initialize()
    st_system = st.create_system()
    st_device = st_system.create_first_device()
    st_datastream = st_device.create_datastream()
    st_datastream.start_acquisition(i)
    st_device.acquisition_start()
    remote_nodemap = st_device.remote_port.nodemap # impossible to pick it, so combined into the main program

    while st_datastream.is_grabbing: # A while loop for acquiring data and check status

        start = time.time()

        data = camera.loop(st_datastream) # data from the camera.py

        if len(data) > 1:
            q.put(data) # To show the image on GUI
            sim_fact = judge.judgement(data) # template matching and similarity factor

            if sim_fact > 0.9:
                ok = "OK"
                r.put(ok) # for image
                #print(time.time() - start)

            else: #
                ng = "NG"
                r.put(ng) # for image
                root = tk.Tk() # for not showing the TK frame
                root.withdraw() # for not showing the TK frame
                trigger.edit_enumeration(remote_nodemap, PIXEL_FORMAT, 1)
                # メッセージボックス（情報）
                messagebox.showerror('NG', '落丁検知')
                trigger.edit_enumeration(remote_nodemap, PIXEL_FORMAT, 0)

        else: # lem(data) < 0
            none = "None"
            r.put(none)

# convert the image from nupy to image for the TK
def converter(q, s):
    while True:
        image_tk = image_convert.converter_canvas(q.get())
        s.put(image_tk)

class Mainloop(tk.Frame):
    def __init__(self, r, master=None):
        super().__init__(master)
        #self.pack()

        self.start_x = 0
        self.increment_OK = 0
        self.increment_NG = 0
        self.failure = 0
        self.total = 0


        #フレームを入れ子で作成。「frame」の中に「canvas」を作成
        frame1 = tk.Frame(root, )
        frame1.place(x=10, y=10, width=canvas_width, height=canvas_height)
        ### キャンバス作成・配置
        self.canvas1 = tk.Canvas(frame1, width=canvas_width, height=canvas_height, background="#fff")
        self.canvas1.place(x=5, y=5)

        #フレームを入れ子で作成。「frame」の中に「canvas」を作成
        frame2 = tk.Frame(root, )
        frame2.place(x=535, y=10, width=canvas_width, height=canvas_height)
        ### キャンバス作成・配置
        self.canvas2 = tk.Canvas(frame2, width=canvas_width, height=canvas_height, background="#fff")
        self.canvas2.place(x=5, y=5)

        #button = tk.Button(text='ボタン', width=30, command=self.thread)
        #button.place(x=5, y=400)
        #button.bind('<Button-1>', )

        self.text1= tk.StringVar()
        self.text1.set("OK")
        self.text_pos = tk.Label(textvariable=self.text1)
        self.text_pos.place(x=5, y=350)

        self.text2= tk.StringVar()
        self.text2.set("NG")
        self.text_pos = tk.Label(textvariable=self.text2)
        self.text_pos.place(x=5, y=390)

        self.text3= tk.StringVar()
        self.text3.set("失敗")
        self.text_pos = tk.Label(textvariable=self.text3)
        self.text_pos.place(x=5, y=430)

        self.text4= tk.StringVar()
        self.text4.set("合計")
        self.text_pos = tk.Label(textvariable=self.text4)
        self.text_pos.place(x=5, y=470)

        self.text5= tk.StringVar()
        self.text5.set("システム")
        self.text_pos = tk.Label(textvariable=self.text5)
        self.text_pos.place(x=5, y=510)

        self.thread()

    def ui_update(self, r):
        while True:
            self.r = r.get()

            self.total += 1
            self.text4.set("合計" + " " + str(self.total))

            if not "None" in self.r:
                if self.start_x is not 0:
                    if self.r == "OK":
                        self.increment_OK += 1
                        self.text1.set("OK" + " " + str(self.increment_OK))
                    else:
                        self.increment_NG += 1
                        self.text2.set("NG" + " " + str(self.increment_NG))
                else:
                    if self.r == "OK":
                        self.increment_OK += 1
                        self.text1.set("OK" + " " + str(self.increment_OK))
                    else:
                        self.increment_NG += 1
                        self.text2.set("NG" + " " + str(self.increment_NG))
            else:
                self.failure += 1
                self.text3.set("失敗" + " " + str(self.failure))

    #@pyqtSlot(str)
    def canvas_update(self, s):
        # Canvasウィジェットを配置し、各種イベントを設定
        #self.canvas1.pack() # disable due to layout of the canvas1 is shifted
        self.canvas1.bind("<ButtonPress-1>", self.start_point_get)
        self.canvas1.bind("<Button1-Motion>", self.rect_drawing)
        self.canvas1.bind("<ButtonRelease-1>", self.release_action)

        while True:
            self.s = s.get()
            self.image_tk = ImageTk.PhotoImage(self.s)

            if self.start_x is not 0:
                # 画像の描画
                self.canvas1.create_image(
                    #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                    #self.canvas_height / 2,
                    0, 0, image=self.image_tk, anchor='nw')

                self.canvas1.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='white')

            else:
                # show the image
                self.canvas1.create_image(
                    #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                    #self.canvas_height / 2,
                    0, 0, image=self.image_tk, anchor='nw')

    # ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
    def start_point_get(self, event):
        global start_x, start_y # グローバル変数に書き込みを行なうため宣言

        self.canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除

        # canvas上に四角形を描画（rectangleは矩形の意味）
        self.canvas1.create_rectangle(event.x,
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
        self.canvas1.coords("rect1", start_x, start_y, end_x, end_y)
    # ドラッグを離したときのイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
    def release_action(self, event):

        # "rect1"タグの画像の座標を元の縮尺に戻して取得
        self.start_x, self.start_y, self.end_x, self.end_y = [
            round(n * RESIZE_RETIO) for n in self.canvas1.coords("rect1")
        ]

        # 取得した座標の部分を切り出し
        coordination = pyautogui.confirm(text="検索範囲に指定しますか?", title="検索範囲", buttons=["Yes","No"])

        if coordination == "Yes":

            # show image on canvas1
            self.canvas1.create_image(
                #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                #self.canvas_height / 2,
                0, 0, image=self.image_tk, anchor='nw')

            #show white line on canvas1
            self.canvas1.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='white')

            # show image on canvas2
            self.image_tk2 = self.canvas_clipper("a")
            self.canvas2.create_image(
                #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                #self.canvas_height / 2,
                canvas_width/2, canvas_height/2, image=self.image_tk2)

        else:
            # show image on canvas1
            self.canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除
            self.canvas1.create_image(
                #self.canvas_width / 2,       # 画像表示位置(Canvasの中心)
                #self.canvas_height / 2,
                0, 0, image=self.image_tk, anchor='nw')
            #self.canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除
            pass

    def canvas_clipper(self, data):
        out_image = np.array(self.s, dtype=np.uint8)

        # サンプル1の切り出し、保存
        img = out_image[self.start_y : self.end_y, self.start_x : self.end_x]
        nparr = np.ascontiguousarray(img, np.uint8) # convert the data into numpy
        image_tk = image_convert.converter_clipper(nparr)
        image_tk = ImageTk.PhotoImage(image_tk)

        return image_tk

    def thread(self):
        thread1 = threading.Thread(target=self.ui_update, args=(r, ))
        thread2 = threading.Thread(target=self.canvas_update, args=(s, ))
        thread1.start()
        thread2.start()

if __name__ == "__main__":

    # supported between instances of 'type' and 'int'
    q = Queue()
    r = Queue()
    s = Queue()

    with pool.Pool(processes=2) as p:

        #multiprocessing
        p0 = p.Process(target=main, args=(q, r, ), daemon=True)
        p1 = p.Process(target=converter, args=(q, s, ), daemon=True)

        p0.start()
        p1.start()



    root = tk.Tk()
    root.title("Hello World")
    root.geometry("1060x550")
    app = Mainloop(r, master = root)
    app.mainloop()

