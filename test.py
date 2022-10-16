#途中でプログラムが停止する→カメラの設定の問題のあ可能性あり
#judgeについて、選択した範囲を検索する用プログラムするmainからの画像を保存する

# https://imagingsolution.net/program/python/tkinter/display_opencv_video_canvas/

from multiprocessing import Process, Queue, pool
import threading
import tkinter as tk
import serial
import loop
import tempfile

#command_mes_val = "%EE#R"+ RMD +"1"+"\r"
command_mes_val = b"%EE#RMD1**\r\n"
command_init = b"%EE#INT\r\n"
command_analog = b"%EE#RAH1\r\n"
command_test = b"%EE#INT**\r\n"
command_zero_set = b"%EE#WZS11**\r\n"

def zero_set_click(value0, value1):
    if value0 and value1 == 0 and 1:
        return 0
    else:
        with tempfile.NamedTemporaryFile(mode='w+') as tf:
            tf.write(str(value1))
            tf.seek(0)
            #tf = tf.read()
            return tf

def main(q):
    # setting for comport
    while True:

        loop_runout = loop.loop(com, command_mes_val)
        q.put(loop_runout)
        value = 0

        #print(zero_set)
        #if zero_set == 1:
        #    zero_set = 0
        #    print("zero_set = 1")
        #    loop.loop(com, command_zero_set)
        #else:
        #    loop_runout = loop.loop(com, command_mes_val)
        #    q.put(loop_runout)

class Mainloop(tk.Frame):
    def __init__(self, q, master=None):
        super().__init__(master)
        #self.pack()

        button = tk.Button(text='ボタン', width=30, command=lambda: zero_set_click(0, 1))
        button.place(x=5, y=400)
        button.bind('<Button-1>', )

        self.text1 = tk.StringVar()
        self.text1.set("OK")
        self.text_pos = tk.Label(textvariable=self.text1,text="Arial 20", font=("Arial", 20))
        self.text_pos.place(x=100, y=100)

        self.thread()

    def ui_update(self, q):
        while True:
            self.q = q.get()
            self.text1.set("振れ量[um]" + " " + str(self.q))

    def thread(self): # threading
        thread1 = threading.Thread(target=self.ui_update, args=(q, ))
        thread1.start()

if __name__ == "__main__":
    # supported between instances of 'type' and 'int'
    q = Queue()
    r = Queue()

    with pool.Pool(processes=1) as p:

        #multiprocessing
        p0 = p.Process(target=main, args=(q, ), daemon=True)
        p0.start()

    root = tk.Tk()
    root.title("Hello World")
    root.geometry("1485x735")
    app = Mainloop(q, master = root)
    app.mainloop()

com = serial.Serial("COM6", 115200, timeout=0.05)
com.is_open