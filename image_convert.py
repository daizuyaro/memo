# Image scale when displaying using OpenCV.
DISPLAY_RESIZE_FACTOR = 1

import cv2 as cv
from PIL import Image, ImageTk

def converter_canvas(data):
    #画像読み込み
    image = data

    #Resize image.and display.
    nparr = cv.resize(image, None,
                       fx=DISPLAY_RESIZE_FACTOR,
                       fy=DISPLAY_RESIZE_FACTOR,
                      )

    #h, w = nparr.shape[:2] #################
    #cvh = 500*h/w #################
    #image_bgr = cv.resize(nparr, (500,int(cvh))) #################
    #画像をBGR→RGB→PIL→ImageTkフォーマットへ変換
    image_rgb = cv.cvtColor(nparr, cv.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)

    return image_pil

# Image scale when displaying using OpenCV.
DISPLAY_RESIZE_FACTOR = 1

import cv2 as cv
from PIL import Image, ImageTk


def converter_clipper(data):
    #画像読み込み
    image = data

    #Resize image.and display.
    nparr = cv.resize(image, None,
                      fx=DISPLAY_RESIZE_FACTOR,
                      fy=DISPLAY_RESIZE_FACTOR,
                      )

    h, w = nparr.shape[:2] #################
    #cvh = 500*h/w #################
    #image_bgr = cv.resize(nparr, (500,int(cvh))) #################
    #cvh = 300*h/w #################
    #image_bgr = cv.resize(nparr, (300,int(cvh))) #################
    #画像をBGR→RGB→PIL→ImageTkフォーマットへ変換
    image_rgb = cv.cvtColor(nparr, cv.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)

    return image_pil