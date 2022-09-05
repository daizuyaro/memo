# judge the photo from the camera
# http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html

import cv2 as cv
import numpy as np
#from matplotlib import pyplot as plt

def judgement(data):
    img = data # numpy data in
    template = cv.imread("D:\\Programing\\PycharmProjects\\image_processing\\data\\b.jpg",0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    #methods = ['cv.TM_CCOEFF']#['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
               #'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    method = eval('cv.TM_CCOEFF')
    #Apply template Matching
    print(img)
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    return(max_val)