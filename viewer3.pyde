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

record = False
recordPath = "/home/carlos/Escritorio/depth-footage/1422478873.oni"

steps = 4
framenumber = 0
offset = 0
oldoffset = 0

footage_folder = "/home/carlos/Escritorio/depth-footage"
folder = recordPath.rpartition("/")[2].rpartition(".")[0]+"_oni_"+str(steps)
filename = ""
filepath = os.path.join(footage_folder, folder)

frames = {}

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
    global context
    global rgbImage, depthImage, depthMap
    global width, height

    context = SimpleOpenNI(this,recordPath)
    width = context.rgbWidth()
    height = context.rgbHeight()
    size(2 * width + 10,height) 
    print("curFramePlayer: " + str(context.curFramePlayer()))
    # disable mirror
    context.setMirror(False)
    # enable depthMap generation 
    context.enableDepth()
    context.enableRGB()
    # align depth data to image data
    context.alternativeViewPointDepthToImage()
    context.setDepthColorSyncEnabled(True)

    

def draw():
    global context, framenumber, width, height
    global rgbImage, depthImage, depthMap
    global record, folder, filename, frames
    global offset, oldoffset
    # update
    context.update()
    background(0, 100, 0)

    rgbImage = context.rgbImage()
    depthImage = context.depthImage()
    depthMap = context.depthMap()
    realWorldMap = context.depthMapRealWorld()

    xyz = []
    for y in [a for a in range(height) if (a%steps == 0)]:
        for x in [a for a in range(width) if (a%steps == 0)]:            
            try:
                index = x + y * width
                pixelColor = rgbImage.pixels[index]

                argb = pixelColor
                r = (argb >> 16) & 0xFF
                g = (argb >> 8) & 0xFF
                b = argb & 0xFF
                color = str(r) + " " + str(g) + " " + str(b)

                point = realWorldMap[index]
                #print("{}x{}: {} {}".format(x+1, y+1, point, pixelColor))
                if point.mag() != 0:
                    xyz.append(str(round(point.x, 3)) + " " + str(round(point.y, 3)) + " " + str(round(point.z, 3)) + " " + color)
            except IndexError:
                pass
    totalframes = context.framesPlayer()
    currentframe = context.curFramePlayer() 
    
    # draw the cam data
    if ((context.nodes() & SimpleOpenNI.NODE_DEPTH) != 0):
        if ((context.nodes() & SimpleOpenNI.NODE_IMAGE) != 0):
            image(depthImage, 0, 0) 
            if not os.path.isfile(filename):
                #image(rgbImage, context.depthWidth() + 10, 0)
                for y in [a for a in range(height) if (a%steps == 0)]:
                    for x in [a for a in range(width) if (a%steps == 0)]:
                        try:
                            index = x + y * width
                            pixelColor = rgbImage.pixels[index]

                            argb = pixelColor
                            r = (argb >> 16) & 0xFF
                            g = (argb >> 8) & 0xFF
                            b = argb & 0xFF
                            noStroke()
                            fill(r,g,b)
                            ellipse(x+width+10,y,steps, steps)
                        except IndexError:
                            pass    
            else:
                image(rgbImage, width+10, 0)
        else:
            image(depthImage, 0, 0)

    filename = os.path.join(filepath,os.path.join(str(currentframe).zfill(6) + ".ply"))

    if record == True:
        
        if filename in frames.keys() or os.path.isfile(filename):
            print("."),
        else:
            frames[filename] = (rgbImage.clone(), xyz)
            print("{} ".format(filename.rpartition("/")[2].rpartition(".")[0])),
            framenumber +=1
    

    #              _ 
    #   __ _ _   _(_)
    #  / _` | | | | |
    # | (_| | |_| | |
    #  \__, |\__,_|_|
    #  |___/         



    #drawgui()
    fill(255,0,0)
    textSize(20)
    # draw frame number
    text("Frame: " + str(context.curFramePlayer()),10,10,120,110)
    if os.path.isfile(filename):
        fill(0,255,0)
    else:
        fill(255,0,0)
    label2 = "{}/{} frames   {} steps  speed {}".format(currentframe, totalframes, steps, context.playbackSpeedPlayer())
    textSize(40)
    text(label2, 50, height - 50)
    
    if record == True:
        if oldoffset == 0:
            oldoffset = currentframe
        offset = currentframe - oldoffset - framenumber + 1
        if offset != 0:
            fill(255,255,0,255)
        else:
            fill(0,255,0,255)
        label1 = "frame:{} {} offset {}".format(framenumber, filename, offset)
        textSize(20)
        text(label1, 50, 50)
        fill(255,0,0,200)
    else:
        fill(0,0,0,75)
    ellipse(width*2 - 50, 50, 70, 70)

    #drawTimeline()
    pushStyle()
    strokeWeight(4)
    stroke(255,255,0)
    line(5, height - 20, width*2 -10 ,height - 20)  
    stroke(0)
    rectMode(CENTER)
    fill(255,255,0)
    pos = int((width*2 - 2 * 10) * currentframe/totalframes)
    rect(pos, height - 20, 7,17)  
    popStyle()











            
def write_frame(data, filename):
    with open(filename, "w") as text_file:
        for line in data:
            text_file.write(line + "\n")

def test_export(frames):
    lista = frames.keys()
    lista.sort()
    print("saving {} frames from {} to {}".format(len(lista),
            lista[0].rpartition("/")[2], 
            lista[len(lista)-1].rpartition("/")[2]))
    for frame in lista:
        points = []
        data = []
        # for y in [a for a in range(height) if (a%steps == 0)]:
        #     for x in [a for a in range(width) if (a%steps == 0)]:            
        #         index = x + y * width
        #         # get the color of the point
        #         #pixelColor = frames[frame][0].get(x,y)
        #         try:
        #             pixelColor = frames[frame][0].pixels[index]
        #             argb = pixelColor
        #             r = (argb >> 16) & 0xFF
        #             g = (argb >> 8) & 0xFF
        #             b = argb & 0xFF
        #             color = str(r) + " " + str(g) + " " + str(b)
                    
        #             point = realWorldMap[index]
                    
        #             #print("{}x{}: {} {}".format(x+1, y+1, point, pixelColor))
        #             if point.mag() != 0:
        #                 points.append(str(round(point.x, 3)) + " " + 
        #                     str(round(point.y, 3)) + " " + str(round(point.z, 3)) + " " + color)
        #         except IndexError:
        #             pass
        #         points.append(str(round(point.x, 3)) + " " + 
        #             str(round(point.y, 3)) + " " + str(round(point.z, 3)) + " " + color)
        # index = 0
        # data.append(header.format(len(points)))
        # for i in points:
        #     data.append(i)
        
        #write_frame(data, frame)
        print("///////{}".format(frame))
        print(frame.rpartition(".")[0].rpartition("/")[2] + " "),














def export(frames):
    lista = frames.keys()
    lista.sort()
    print("saving {} frames from {} to {}".format(len(lista),
            lista[0].rpartition("/")[2], 
            lista[len(lista)-1].rpartition("/")[2]))
    for frame in lista:
        points = []
        data = []
        # for y in [a for a in range(height) if (a%steps == 0)]:
        #     for x in [a for a in range(width) if (a%steps == 0)]:            
        #         index = x + y * width
        #         # get the color of the point
        #         #pixelColor = frames[frame][0].get(x,y)
        #         try:
        #             pixelColor = frames[frame][0].pixels[index]
        #             argb = pixelColor
        #             r = (argb >> 16) & 0xFF
        #             g = (argb >> 8) & 0xFF
        #             b = argb & 0xFF
        #             color = str(r) + " " + str(g) + " " + str(b)           
        #             point = frames[frame][1][index]
        #             #point = frames[frame][1][x][y]
        #             if not (point.x == 0 and point.y == 0 and point.z == 0):
        #                 points.append(str(round(point.x, 3)) + " " + 
        #                     str(round(point.y, 3)) + " " + str(round(point.z, 3)) + " " + color)
        #         except IndexError:
        #             pass
        #         #points.append(str(round(point.x, 3)) + " " + 
        #         #    str(round(point.y, 3)) + " " + str(round(point.z, 3)) + " " + color)
        index = 0

        xyz = frames[frame][1]
        data.append(header.format(len(xyz)))
        for line in xyz:
            data.append(line)
        
        write_frame(data, frame)
        #print(frame)
        print(frame.rpartition(".")[0].rpartition("/")[2] + " "),












def keyPressed():
    global context, record, folder, framenumber, offset, oldoffset, frames, steps

    if keyPressed:
        if key == "r" or key == "R":
            record = True
            print("NOW recording frames into memory-------------------------")
        if key == "s" or key =="S":
            if record == True:
                if len(frames) > 0:
                    noLoop()
                    print("NOW saving files in {} ------------".format(filepath))
                    if not os.path.isdir(filepath):
                        os.system("mkdir {}".format(filepath))
                    export(frames)
                    frames = {}
                    loop()
                record = False
                framenumber = 0
                offset = 0
                oldoffset = 0
        if key == "t" or key =="T":
            if record == True:
                if len(frames) > 0:
                    noLoop()
                    print("NOW saving files in {} ------------".format(filepath))
                    if not os.path.isdir(filepath):
                        os.system("mkdir {}".format(filepath))
                    test_export(frames)
                    frames = {}
                    loop()
                record = False
                framenumber = 0
                offset = 0
                oldoffset = 0

    if key == CODED:
        if keyCode == RIGHT:
            steps += 1
        if keyCode == LEFT:
            steps -= 1
            if steps == 0:
                steps = 1
        if keyCode == UP:
            # speed up
            context.setPlaybackSpeedPlayer(context.playbackSpeedPlayer() * 0.5)
            println("playbackSpeedPlayer: " + str(context.playbackSpeedPlayer()))  
        if keyCode == DOWN:
            # slow down
            context.setPlaybackSpeedPlayer(context.playbackSpeedPlayer() * 2.0)
            print("playbackSpeedPlayer: " + str(context.playbackSpeedPlayer()))
            