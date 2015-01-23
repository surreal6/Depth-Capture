"""
/* --------------------------------------------------------------------------
 * SimpleOpenNI AlternativeViewpoint3d Test
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

if context.isInit() == False:   
    print("Can't init SimpleOpenNI, maybe the camera is not connected!") 
    sys.exit()

zoomF = 0.3
rotX = radians(180)  
# by default rotate the hole scene 180deg around the x-axis 
# the data from openni comes upside down
rotY = radians(0)
#PShape       pointCloud
steps = 2

def setup():
    size(1024, 768, P3D)

    # disable mirror
    #context.setMirror(False)

    # enable depthMap generation 
    #context.enableDepth()

    #context.enableRGB()
    
    print("size: {}x{}".format(context.rgbWidth(), context.rgbHeight()))
 
    # align depth data to image data
    # context.alternativeViewPointDepthToImage()
    # context.setDepthColorSyncEnabled(True)
 
    # stroke(255,255,255)
    # smooth()
    # perspective(radians(45), float(width)/float(height), 10, 150000)


def draw():
    # update the cam
    #context.update()

    background(0,0,0)

    # translate(width/2, height/2, 0)
    # rotateX(rotX)
    # rotateY(rotY)
    # scale(zoomF)

    # rgbImage = context.rgbImage()
    # depthMap = context.depthMap()
    # steps = 4  # to speed up the drawing, draw every third point
    # #int     index
    # #PVector realWorldPoint
    # #color   pixelColor
 
    # strokeWeight((float(steps)/2))

    # translate(0,0,-1000)  # set the rotation center of the scene 1000 infront of the camera

    # realWorldMap = context.depthMapRealWorld()
    # beginShape(POINTS)
    # x = 0
    # y = 0
    # while y < context.depthHeight():
    #     while x < context.depthWidth():
    #         index = x + y * context.depthWidth()
    #         if depthMap[index] > 0:
    #             # get the color of the point
    #             pixelColor = rgbImage.pixels[index]
    #             stroke(pixelColor)
                
    #             # draw the projected point
    #             realWorldPoint = realWorldMap[index]
    #             vertex(realWorldPoint.x,realWorldPoint.y,realWorldPoint.z)  # make realworld z negative, in the 3d drawing coordsystem +z points in the direction of the eye
    #         x += steps
    #     y += steps
        
     
    # endShape()
    
    # # draw the kinect cam
    # strokeWeight(1)
    # context.drawCamFrustum()



# def keyPressed():

#     switch(key)
    
#     case ' ':
#         context.setMirror(!context.mirror())
#         break
    

#     switch(keyCode)
    
#     case LEFT:
#         rotY += 0.1f
#         break
#     case RIGHT:
#         # zoom out
#         rotY -= 0.1f
#         break
#     case UP:
#         if(keyEvent.isShiftDown())
#             zoomF += 0.02f
#         else
#             rotX += 0.1f
#         break
#     case DOWN:
#         if(keyEvent.isShiftDown())
        
#             zoomF -= 0.02f
#             if(zoomF < 0.01)
#                 zoomF = 0.01
        
#         else
#             rotX -= 0.1f
#         break
    


