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

import sys, time, os

context = SimpleOpenNI(this)
# disable mirror
context.setMirror(False)

# enable depthMap generation 
context.enableDepth()
context.enableRGB()

rgbImage = context.rgbImage()
depthImage = context.depthImage()
depthMap = context.depthMap()

width = context.rgbWidth()
height = context.rgbHeight()

steps = 4
framenumber = 0
capture = False
record = False
folder = ""

recording = []

header = """ply
format ascii 1.0
comment VCGLIB generated
element vertex {}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element face 0
property list uchar int vertex_indices
end_header"""

def setup():
    size(width, height)

    print("size: {}x{}".format(context.rgbWidth(), context.rgbHeight()))
 
    # align depth data to image data
    context.alternativeViewPointDepthToImage()
    context.setDepthColorSyncEnabled(True)

def read_frame():
    realWorldMap = context.depthMapRealWorld()
    
    points = []
    data = []
    for y in [a for a in range(height) if (a%steps == 0)]:
        for x in [a for a in range(width) if (a%steps == 0)]:            
            index = x + y * width
            
            # get the color of the point
            pixelColor = rgbImage.pixels[index]
            argb = pixelColor
            r = (argb >> 16) & 0xFF
            g = (argb >> 8) & 0xFF
            b = argb & 0xFF
            color = str(r) + " " + str(g) + " " + str(b)

            point = realWorldMap[index]

            #print("{}x{}: {} {}".format(x+1, y+1, point, pixelColor))
            if point.mag() != 0:
                points.append(str(round(point.x, 3)) + " " + str(round(point.y, 3)) + " " + str(round(point.z, 3)) + " " + color)
    data.append(header.format(len(points)))
    for i in points:
    	data.append(i)
    return data
            
def write_frame(data, filename):
    with open(filename, "w") as text_file:
        for line in data:
            text_file.write(line + "\n")


def draw():
    global rgbImage, depthImage, depthMap, capture, framenumber, recording

    # update the cam
    context.update()

    background(0,0,0)

    rgbImage = context.rgbImage()
    depthImage = context.depthImage()
    depthMap = context.depthMap()
    
    # draw depthImageMap
    image(depthImage, 0, 0)

    if capture:
        filename = str(int(time.time()))+".ply"
        data = read_frame()
        write_frame(data, filename)
        capture = False

    if record:
    	data = read_frame()
        recording.append((framenumber, data, time.time()))
        if len(recording) > 10:
        	for frame in recording:
        		filename = os.path.join("./" + folder, str(frame[0])+".ply")
        		write_frame(frame[1], filename)
        		print(filename)
        	recording = []
        framenumber +=1 
        
    

def keyPressed():
    global capture, record, folder, framenumber
    
    if keyPressed:
        # (C)apture frame
        if key == "c":
            if capture == True:
                capture = False
            else:
                capture = True
        # (S)top recording
        if key == "s":
            if record == True:
                record = False
                folder = ""
                framenumber = 0
        # start (R)ecording
        if key == "r":
            folder = str(int(time.time()))

            os.system("mkdir " + folder)
            os.system("cd " + folder)
            record = True




    # if key == CODED:
    #     if keyCode == RIGHT:

    #     if keyCode == LEFT:

    #     if keyCode == UP:

    #     if keyCode == DOWN:

        
    





