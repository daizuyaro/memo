"""
 This sample shows how to set ROI in camera side and handle the image data.
 The following points will be demonstrated in this sample code:
 - Initialize StApi
 - Connect to camera
 - Set image ROI parameter
 - Acquire image data
 - Process the acquired ROI images
"""
import stapipy as st
# Feature names
PIXEL_FORMAT = "UserOutputValue0"

def edit_enumeration(nodemap, enum_name, value) -> bool:
    """
    Display and edit enumeration value.
    :param nodemap: Node map.
    :param enum_name: Enumeration name.
    :return: True if enumeration value is updated. False otherwise.
    """
    node = nodemap.get_node(enum_name)
    enum_node = st.PyIBoolean(node)
    enum_node.set_value(value)
    enum_entries = enum_node.value
    print(enum_entries)

#try:
#    # Initialize StApi before using.
#    st.initialize()
#    # Create a system object for device scan and connection.
#    st_system = st.create_system()
#    # Connect to first detected device.
#    st_device = st_system.create_first_device()
#    # Display DisplayName of the device.
#    #print('Device=', st_device.info.display_name)
#    # Create a datastream object for handling image stream data.
#    #st_datastream = st_device.create_datastream()
#    # Get INodeMap object to access the setting of the device.
#    remote_nodemap = st_device.remote_port.nodemap
#    # Check and set PixelFormat
#    edit_enumeration(remote_nodemap, PIXEL_FORMAT)

#except Exception as exception:
#    print(exception)