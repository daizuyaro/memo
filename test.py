import numpy as np
from stapipy import PyStImage

# ROI setting
pos_x = 864 # offset x
pos_y = 648 # offset y
width = 884 # wideth
height = 668 # height

def loop(st_image):
    st_image = PyStImage.get_roi_image(st_image, pos_x, pos_y, width, height) # ROI in manual (clip a image from the original photo)
    data = st_image.get_image_data() # get the image from the data
    nparr = np.frombuffer(data, np.uint8) # convert the data into numpy
    nparr = nparr.reshape(st_image.height, st_image.width) # Process image for display.

    return nparr