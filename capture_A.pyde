"""
/* --------------------------------------------------------------------------
 * SimpleOpenNI Record/Play Test
 * --------------------------------------------------------------------------
 * Processing Wrapper for the OpenNI/Kinect 2 library
 * http:#code.google.com/p/simple-openni
 * --------------------------------------------------------------------------
 * prog:  Max Rheiner / Interaction Design / Zhdk / http:#iad.zhdk.ch/
 * date:  12/12/2012 (m/d/y)
 * ----------------------------------------------------------------------------
 * For playing the recorded file, just set recordFlag to False
 * All files should be in the data subfolder of the current project, abs.
 * path work as well
 * ----------------------------------------------------------------------------
 */
"""
import time, math

recordPath = "./" + str(time.time()).rpartition(".")[0] + ".oni"

from SimpleOpenNI import SimpleOpenNI

context = SimpleOpenNI(0 ,this,SimpleOpenNI.RUN_MODE_MULTI_THREADED)
if context.isInit() == False:
    print("Can't init SimpleOpenNI, maybe the camera is not connected!") 
    exit()

x = 0

def setup():
    global context

    size(2 * 640 + 10,480) 
    # recording
    # disable mirror
    context.setMirror(False)
    # enable depthMap generation 
    context.enableDepth()
    context.enableRGB()

    recordFlag = True
    # setup the recording 
    context.enableRecorder(recordPath)
    # nodes
    context.addNodeToRecording(SimpleOpenNI.NODE_DEPTH,True)
    context.addNodeToRecording(SimpleOpenNI.NODE_IMAGE,True)
        

def draw():
    global context, x

    # update
    context.update()
    background(200, 0, 0)
    # draw the cam data
    if ((context.nodes() and SimpleOpenNI.NODE_DEPTH) != 0):
        if ((context.nodes() and SimpleOpenNI.NODE_IMAGE) != 0):
            image(context.depthImage(), 0, 0)   
            image(context.rgbImage(), context.depthWidth() + 10, 0)
        else:
            image(context.depthImage(), 0, 0)


    drawgui()
    x += 1

def drawgui():
    fill(255,0,0, math.sin(x*0.3)*255)
    stroke(255,0,0)
    strokeWeight(3)
    ellipse(1280-50, 50, 50,50)
    
    
    fill(255,0,0)
    stroke(255,0,0)

    label1 = "frame::  folder: ".format(x, recordPath)
    textSize(15)
    text(label1, 50, 50) 
