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
import time, os, sys

from SimpleOpenNI import SimpleOpenNI

recordPath = ""

def setup():
    selectInput("Select a file to process:", "fileSelected")
    
    global context
    size(2 * 640 + 10,480) 

    context = SimpleOpenNI(this,recordPath)
    print("curFramePlayer: " + str(context.curFramePlayer()))
    # disable mirror
    context.setMirror(False)

def fileSelected(selection):
    global recordPath

    if selection == None:
        print("Window was closed or the user hit cancel.")
        recordPath = ""
    else:
        print("User selected " + selection.getAbsolutePath())
        recordPath = selection.getAbsolutePath()
    print("------------",recordPath, selection)
    
    

def draw():
    global context
    # update
    context.update() 
    background(200, 0, 0)
    # draw the cam data
    if ((context.nodes() & SimpleOpenNI.NODE_DEPTH) != 0):
        if ((context.nodes() & SimpleOpenNI.NODE_IMAGE) != 0):
            image(context.depthImage(), 0, 0)   
            image(context.rgbImage(), context.depthWidth() + 10, 0)
        else:
            image(context.depthImage(), 0, 0)
    # draw frame number
    text("Frame: " + str(context.curFramePlayer()),10,10)



