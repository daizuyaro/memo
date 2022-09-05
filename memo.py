import tkinter as tk
import pyautogui  # 外部ライブラリ
from PIL import Image, ImageTk  # 外部ライブラリ

RESIZE_RETIO = 2 # 縮小倍率の規定

# ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
def start_point_get(event):
    global start_x, start_y # グローバル変数に書き込みを行なうため宣言

    canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除

    # canvas1上に四角形を描画（rectangleは矩形の意味）
    canvas1.create_rectangle(event.x,
                                  event.y,
                                  event.x + 1,
                                  event.y + 1,
                                  outline="white",
                                  tag="rect1")
    # グローバル変数に座標を格納
    start_x, start_y = event.x, event.y

# ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
def rect_drawing(event):

    # ドラッグ中のマウスポインタが領域外に出た時の処理
    if event.x < 0:
        end_x = 0
    else:
        end_x = min(img_resized.width, event.x)
    if event.y < 0:
        end_y = 0
    else:
        end_y = min(img_resized.height, event.y)

    # "rect1"タグの画像を再描画
    canvas1.coords("rect1", start_x, start_y, end_x, end_y)

# ドラッグを離したときのイベント - - - - - - - - - - - - - - - - - - - - - - - - - -
def release_action(event):

    # "rect1"タグの画像の座標を元の縮尺に戻して取得
    start_x, start_y, end_x, end_y = [
        round(n * RESIZE_RETIO) for n in canvas1.coords("rect1")
    ]

    # 取得した座標の部分を切り出し
    cordination = pyautogui.confirm(text="検索範囲に指定しますか?", title="検索範囲", buttons=["Yes","No"])
    if cordination == "Yes":
        im = Image.open('D:\\Programing\\PycharmProjects\\image_processing\\data\\a.jpg')
        im_crop = im.crop((start_x, start_y, end_x, end_y))
        im_crop.save('D:\\Programing\\PycharmProjects\\image_processing\\data\\b.jpg', quality=100)
        root.destroy()
    else:
        pass

root = tk.Toplevel()

# 表示する画像の取得（スクリーンショット）
#img = pyautogui.screenshot()
img = Image.open('D:\\Programing\\PycharmProjects\\image_processing\\data\\a.jpg')
# スクリーンショットした画像は表示しきれないので画像リサイズ
img_resized = img.resize(size=(int(img.width / RESIZE_RETIO),
                             int(img.height / RESIZE_RETIO)),
                                    resample=Image.BILINEAR)

# tkinterで表示できるように画像変換
img_tk = ImageTk.PhotoImage(img_resized)

# Canvasウィジェットの描画
canvas1 = tk.Canvas(root,
              bg="black",
              width=img_resized.width,
              height=img_resized.height)
# Canvasウィジェットに取得した画像を描画
canvas1.create_image(0, 0, image=img_tk, anchor=tk.NW)

# Canvasウィジェットを配置し、各種イベントを設定
canvas1.pack()
canvas1.bind("<ButtonPress-1>", start_point_get)
canvas1.bind("<Button1-Motion>", rect_drawing)
canvas1.bind("<ButtonRelease-1>", release_action)

root.title("Hello World")
root.attributes("-topmost", True) # tkinterウィンドウを常に最前面に表示
root.mainloop()