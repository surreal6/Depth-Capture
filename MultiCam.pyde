"""
/* --------------------------------------------------------------------------
 * SimpleOpenNI Multi Camera Test   ---   py-processing
 * --------------------------------------------------------------------------
 * Processing Wrapper for the OpenNI/Kinect 2 library
 * http://code.google.com/p/simple-openni
 * --------------------------------------------------------------------------
 * prog:  Max Rheiner / Interaction Design / Zhdk / http://iad.zhdk.ch/
 * date:  12/12/2012 (m/d/y)
 * ----------------------------------------------------------------------------
 * Be aware that you shouln't put the cameras at the same usb bus !!!!!!!!!!!!!!!!!
 * On linux/OSX  you can use the command 'lsusb' to see on which bus the camera is
 * ----------------------------------------------------------------------------
 */
"""

from SimpleOpenNI import SimpleOpenNI
from SimpleOpenNI import StrVector

# print all the cams
strList = StrVector()
print(strList)
SimpleOpenNI.deviceNames(strList)
for i in range(strList.size()):
    print("{}: {}".format(i,str(strList.get(i))))

    # check if there are enough cams  
    if strList.size() < 2:
        println("only works with 2 cams")
        exit()

# init the cameras
cam1 = SimpleOpenNI(0 ,this,SimpleOpenNI.RUN_MODE_MULTI_THREADED)
cam2 = SimpleOpenNI(1 ,this,SimpleOpenNI.RUN_MODE_MULTI_THREADED)

if (cam1.isInit() == False or cam2.isInit() == False) :
    print("Verify that you have two connected cameras on two different usb-busses!") 
    exit()

def setup():
    global cam1, cam2

    size(640 * 2 + 10,480 * 2 + 10) 

    # start OpenNI, load the library
    SimpleOpenNI.start()

    # set the camera generators

    # enable depthMap generation 
    cam1.enableDepth()
    cam1.enableRGB()

    # enable depthMap generation 
    cam2.enableDepth()
    cam2.enableRGB()

    background(10,200,20)


def draw():

    # update the cam
    SimpleOpenNI.updateAll()

    # draw depthImageMap
    image(cam1.depthImage(),0,0)
    image(cam1.rgbImage(),0,480 + 10)

    image(cam2.depthImage(),640 + 10,0)
    image(cam2.rgbImage(),640 + 10,480 + 10)
  

