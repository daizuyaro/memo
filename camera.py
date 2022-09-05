# ok!
import numpy as np
import time
from stapipy import PyStImage

# ROI setting
pos_x = 864 # offset x
pos_y = 648 # offset y
width = 864 # wideth
height = 648 # height


def loop(st_datastream):

    timeout = 2678400000 # 31 day x 24 hour x 3600s x 1000ms

    with st_datastream.retrieve_buffer(timeout, 1) as st_buffer:
        if st_buffer.info.is_image_present:
            st_image = st_buffer.get_image() # get the data from the buffer
            st_image = PyStImage.get_roi_image(st_image, pos_x, pos_y, width, height) # ROI in manual (clip a image from the original photo)
            data = st_image.get_image_data() # get the image from the data
            nparr = np.frombuffer(data, np.uint8) # convert the data into numpy
            nparr = nparr.reshape(st_image.height, st_image.width) # Process image for display.

            return nparr
        else:
            return []

            #return "acquision_error"
#st_device.acquisition_stop()
#st_datastream.stop_acquisition()