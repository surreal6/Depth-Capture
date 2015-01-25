"""
/* --------------------------------------------------------------------------
 * KinoDepth: SimpleOpenNI based Recording Software
 * --------------------------------------------------------------------------
 * Processing Wrapper for the OpenNI/Kinect 2 library
 * http:#code.google.com/p/simple-openni
 * --------------------------------------------------------------------------
 * prog:  Carlos Padial / Interaction Design / Kinoraw / http:kinoraw.net/
 * date:  24/01/2015 (m/d/y)
 * ----------------------------------------------------------------------------
 */
 """

from SimpleOpenNI import SimpleOpenNI


import sys, time, os

#context = SimpleOpenNI(this)

context = SimpleOpenNI(0,this,SimpleOpenNI.RUN_MODE_MULTI_THREADED)
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
footage_folder = "/home/carlos/Escritorio/depth-footage"

t1 = str(time.localtime()[5]).zfill(6)
t2 = str(time.time()).rpartition(".")[0]

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

def mkdir(path):
    a = os.system("mkdir {}".format(dir))
    print(a)


def draw():
    global rgbImage, depthImage, depthMap, capture, framenumber 
    global recording, t1, t2, steps, folder
    # update the cam
    context.update()

    background(0,0,0)

    rgbImage = context.rgbImage()
    depthImage = context.depthImage()
    depthMap = context.depthMap()
    
    # draw depthImageMap
    image(depthImage, 0, 0)

    # update timers
    t1 = str(time.localtime()[5]).zfill(6)
    t2 = str(time.time()).rpartition(".")[0]

    if capture:
        filename = os.path.join(footage_folder,t2 +".ply")
        #filename = str(int(time.time()))+".ply"
        data = read_frame()
        write_frame(data, filename)

    if record == True:
        data = read_frame()
        recording.append((t1, t2, data, folder))
        framenumber +=1 
    else:
        if len(recording) != 0:
            for frame in recording:
                folder = frame[3]
                filepath = os.path.join(footage_folder, folder)
                print(filepath)
                filename = os.path.join(filepath, frame[0] + "_" + frame[1] + ".ply")
                write_frame(frame[2], filename)
                print(filename)
            recording = []
            folder = ""
    drawgui()
    capture = False
           
def drawgui():
    
    fill(255,0,0)
    stroke(255,0,0)

    label1 = "frame:{}  {}:{}      {}".format(framenumber, t1, t2, steps)
    textSize(15)
    text(label1, 50, 50) 

    stroke(255,0,0,75)
    strokeWeight(4)
    if record == True or capture == True:
        fill(255,0,0,75)
    else:
        fill(0,0,0,75)
    ellipse(width - 50, 50, 70, 70)





def keyPressed():
    global capture, record, folder, framenumber, steps
    
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
            record = True
            folder = str(time.time()).rpartition(".")[0] + "_" + str(steps)
            path = os.path.join(footage_folder, folder)
            os.system("mkdir {}".format(path))
            print("folder {} created!!".format(path))



    if key == CODED:
        #if keyCode == RIGHT:

        #if keyCode == LEFT:

        if keyCode == UP:
            steps += 1
            if steps > 100:
                steps > 100
        if keyCode == DOWN:
            steps -= 1
            if steps == 0:
                steps = 1
