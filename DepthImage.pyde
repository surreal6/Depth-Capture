"""
/* --------------------------------------------------------------------------
 * SimpleOpenNI DepthImage Test
 * --------------------------------------------------------------------------
 * Processing Wrapper for the OpenNI/Kinect 2 library
 * http:#code.google.com/p/simple-openni
 * --------------------------------------------------------------------------
 * prog:  Max Rheiner / Interaction Design / Zhdk / http:#iad.zhdk.ch/
 * date:  12/12/2012 (m/d/y)
 * ----------------------------------------------------------------------------
 */
 """

from SimpleOpenNI import SimpleOpenNI

import sys

context = SimpleOpenNI(this)

def saveframe(data):
    filename = str(int(time.time()))+".xyz"
    with open(filename, "w") as text_file:
        for line in data:
            text_file.write(line)

def setup():
    size(640*2, 480)

    if context.isInit() == False:
        print("Can't init SimpleOpenNI, maybe the camera is not connected!") 
        exit()
        return

    # mirror is by default enabled
    context.setMirror(True)

    # enable depthMap generation 
    context.enableDepth()

    # enable ir generation
    context.enableRGB()

def draw():
    # update the cam
    context.update()

    background(200, 0, 0)

    # draw depthImageMap
    image(context.depthImage(), 0, 0)

    # draw irImageMap
    image(context.rgbImage(), context.depthWidth() + 10, 0)

    

    #for i in dir(context): print(i)

    # print("deviceCount {} deviceIndex {} depthImageColorMode".format(context.deviceCount(), context.deviceIndex(), context.depthImageColorMode()))
    # print("Field of View {} {}".format(context.vFieldOfView(), context.hFieldOfView()))
    # print("depth {} {} irTimeStamp {}".format(context.depthWidth(), context.depthWidth(), context.irTimeStamp()))
    # print("rgb {} {} sceneTimeStamp {}".format(context.rgbWidth(), context.rgbHeight(), context.sceneTimeStamp()))