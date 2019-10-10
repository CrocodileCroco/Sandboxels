import random
import os
import sys
from colorama import init, Fore, Back, Style
import time
import keyboard
from tkinter import * 
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import threading
from tkinter.simpledialog import askstring
import json
import noise
import requests




root = Tk()

init()

gamemap = []


playerposx = 1
playerposy = 1

barriernames = ["woodbarrier", "stonebarrier"]

def clear(): 
  
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

clear()

mapsize = (100, 100)
#default 64x32

img = Image.new('RGB', (mapsize[0], mapsize[1]), color = 'white')
pixels = img.load()

playerinv = {}



def genmap():
    global gamemap
    global mapsize
    global img
    freq = 16.0 * 1
    octaves = 1
    genh = 1
    seed = np.random.randint(0, 90000)
    print(seed)
    while genh != mapsize[1]:
        gamemap.append([])
        genw = 1
        while genw != mapsize[0]:
            gamemap[genh - 1].append({"blocktype":"grass","blockcolor":(0, int(noise.snoise2(genw / freq, genh / freq, octaves, base=seed) * 127.0 + 128.0), 0)})
            #print(gamemap[genh - 1][-1]["blockcolor"][1])
            if gamemap[genh - 1][-1]["blockcolor"][1] < 80:
                gamemap[genh - 1][-1]["blockcolor"] = (0, 204, 255)
                gamemap[genh - 1][-1]["blocktype"] = "water"
            elif gamemap[genh - 1][-1]["blockcolor"][1] < 110:
                gamemap[genh - 1][-1]["blockcolor"] = (255, 255, 153)
                gamemap[genh - 1][-1]["blocktype"] = "sand"
            else:
                gamemap[genh - 1][-1]["blockcolor"] = (0, 153, 51)
                gamemap[genh - 1][-1]["blocktype"] = "grass"
            genw = genw + 1
        genh = genh + 1
    genh = 1
    while genh != mapsize[1]:
        genw = 1
        while genw != mapsize[0]:
            if gamemap[genh - 1][genw - 1]["blockcolor"] == (0, 153, 51):
                randomtree = random.randint(0,15)
                if randomtree == 15:
                    gamemap[genh - 1][genw - 1] = {"blocktype":"tree","blockcolor":(153, 51, 0)}
            genw = genw + 1
        genh = genh + 1



tkimage = ImageTk.PhotoImage(img)
imglbl = Label(root, image=tkimage)
imglbl.grid(row=0, column=0)

def rendermap():
    global gamemap
    global mapsize
    global img
    global root
    global imglbl
    global tkimage
    global pixels
    zz = 0
    img = Image.new('RGB', (mapsize[0], mapsize[1]), color = 'white')
    for o in range(mapsize[1] - 1):
        i2 = 1
        o2 = o - 1
        i3 = 1
        #print("\n", end='')
        for i in range(mapsize[0] - 1):
            for j in range(mapsize[1] - 1):
                if playerposx == i and playerposy == j:
                    img.putpixel((i,j), (240, 204, 214))
                else:
                    img.putpixel((i,j), gamemap[j][i]["blockcolor"])
        #sys.stdout.write("\n")
    img2 = img.resize(((mapsize[0] * 9),(mapsize[1] * 9)),resample=Image.NEAREST)
    tkimage = ImageTk.PhotoImage(img2)
    imglbl.configure(image=tkimage)

def playermove(movefrom, moveto):
    global gamemap
    global playerposx
    global playerposy
    global selectedbcolor
    global img
    global root
    global imglbl
    global tkimage
    global pixels
    global barriernames
    #print(movefrom, moveto)
    try:
        img.putpixel(movefrom, gamemap[movefrom[1]][movefrom[0]]["blockcolor"])
        img.putpixel(moveto, (240, 204, 214))
        img2 = img.resize(((mapsize[0] * 9),(mapsize[1] * 9)),resample=Image.NEAREST)
        tkimage = ImageTk.PhotoImage(img2)
        imglbl.configure(image=tkimage)
    except:
        print("you are going too far!")
    

genmap()
clear()
rendermap()

selectedbcolor = (163, 163, 163)



def setblock(blocktoset, blocktosetcolor):
    global gamemap
    global playerposx
    global playerposy
    global selectedbcolor
    global img
    global root
    global imglbl
    global tkimage
    global pixels
    global barriernames
    if blocktoset != "nowhere":
        img.putpixel((blocktoset["x"],blocktoset["y"]), blocktosetcolor)
        img2 = img.resize(((mapsize[0] * 9),(mapsize[1] * 9)),resample=Image.NEAREST)
        tkimage = ImageTk.PhotoImage(img2)
        imglbl.configure(image=tkimage)
    

def gameloop():
    global gamemap
    global playerposx
    global playerposy
    global selectedbcolor
    global img
    global root
    global imglbl
    global tkimage
    global pixels
    global barriernames
    
    if keyboard.is_pressed('insert'):
        root.quit()
        sys.exit()
    if keyboard.is_pressed('up'):
        try:
            if gamemap[playerposy - 1][playerposx]["blocktype"] in barriernames:
                print("You can't pass because it's a barrier block")
            else:
                playermove((playerposx, playerposy), (playerposx, playerposy - 1))
                playerposy = playerposy - 1
                time.sleep(0.04)
                #clear()
                #rendermap()
        except:
            print("you are going too far!")
    if keyboard.is_pressed('down'):
        try:
            if gamemap[playerposy + 1][playerposx]["blocktype"] in barriernames:
                print("You can't pass because it's a barrier block")
            else:
                playermove((playerposx, playerposy), (playerposx, playerposy + 1))
                playerposy = playerposy + 1
                time.sleep(0.04)
                #clear()
                #rendermap()
        except:
            print("you are going too far!")
    if keyboard.is_pressed('right'):
        try:
            if gamemap[playerposy][playerposx + 1]["blocktype"] in barriernames:
                print("You can't pass because it's a barrier block")
            else:
                playermove((playerposx, playerposy), (playerposx + 1, playerposy))
                playerposx = playerposx + 1
                time.sleep(0.04)
                #clear()
                #rendermap()
        except:
            print("you are going too far!")
    if keyboard.is_pressed('left'):
        try:
            if gamemap[playerposy][playerposx - 1]["blocktype"] in barriernames:
                print("You can't pass because it's a barrier block")
            else:
                playermove((playerposx, playerposy), (playerposx - 1, playerposy))
                playerposx = playerposx - 1
                time.sleep(0.04)
                #clear()
                #rendermap()
        except:
            print("you are going too far!")
    if keyboard.is_pressed('shift'):
        print("bmode")
        #clear()
        sys.stdout.write(Fore.WHITE + "BuildMode \n")
        bmode = 1
        whereitbuilds = {}
        while bmode == 1:
            if keyboard.is_pressed('right'):
                if gamemap[playerposy][playerposx + 1]["blocktype"] in barriernames:
                    print("you can't build in barriers")
                    bmode = 0
                else:
                    gamemap[playerposy][playerposx + 1] = {"blocktype":"buildblock","blockcolor":selectedbcolor}
                    whereitbuilds = {"x":playerposx + 1,"y":playerposy}
                    bmode = 0
                    print("bmodded")
            if keyboard.is_pressed('left'):
                if gamemap[playerposy][playerposx - 1]["blocktype"] in barriernames:
                    print("you can't build in barriers")
                    bmode = 0
                else:
                    gamemap[playerposy][playerposx - 1] = {"blocktype":"buildblock","blockcolor":selectedbcolor}
                    whereitbuilds = {"x":playerposx - 1,"y":playerposy}
                    bmode = 0
                    print("bmodded")
            if keyboard.is_pressed('down'):
                if gamemap[playerposy + 1][playerposx]["blocktype"] in barriernames:
                    print("you can't build in barriers")
                    bmode = 0
                else:
                    gamemap[playerposy + 1][playerposx] = {"blocktype":"buildblock","blockcolor":selectedbcolor}
                    whereitbuilds = {"x":playerposx,"y":playerposy + 1}
                    bmode = 0
                    print("bmodded")
            if keyboard.is_pressed('up'):
                if gamemap[playerposy - 1][playerposx]["blocktype"] in barriernames:
                    print("you can't build in barriers")
                    bmode = 0
                else:
                    gamemap[playerposy - 1][playerposx] = {"blocktype":"buildblock","blockcolor":selectedbcolor}
                    whereitbuilds = {"x":playerposx,"y":playerposy - 1}
                    bmode = 0
                    print("bmodded")
            if keyboard.is_pressed('esc'):
                bmode = 0
                print("bmodded")
                whereitbuilds = "nowhere"
            if keyboard.is_pressed('space'):
                selectedbcolor = eval("(" + input("RGB Color:") + ")")
                print(selectedbcolor)
                whereitbuilds = "nowhere"
                bmode = 0
                print("bmodded")
        #clear()
        time.sleep(0.1)
        setblock(whereitbuilds, selectedbcolor)
    root.after(1, gameloop)    

commandbar = Entry(root)

def docommand(event):
    global gamemap
    global playerposx
    global playerposy
    global selectedbcolor
    global img
    global root
    global imglbl
    global tkimage
    global pixels
    global commandbar
    global playerinv
    if commandbar.get().startswith("!setcolor"):
        selectedbcolor = eval("(" + commandbar.get()[10:] + ")")
    if commandbar.get() == "!punchtree":
        if gamemap[playerposy][playerposx]["blocktype"] == "tree":
            gamemap[playerposy][playerposx] = {"blocktype":"grass","blockcolor":(0, 153, 51)}
            setblock({"x":playerposx,"y":playerposy},(0, 153, 51))
            playermove((playerposx, playerposy),(playerposx, playerposy))
            if not "wood" in playerinv:
                playerinv["wood"] = 0
            playerinv["wood"] = playerinv["wood"] + 3
            print("You got 3 wood")
            print(playerinv)
        else:
            print("That is not a tree")
    if commandbar.get().startswith("!loadmap"):
        try:
            maploader = open(commandbar.get()[9:], "r")
            gamemap = eval(maploader.read())
            maploader.close()
            rendermap()
            print("Map loaded!")
        except:
            print("Error while loading map")
    if commandbar.get().startswith("!savemap"):
        try:
            maploader = open(commandbar.get()[9:], "w")
            maploader.write(str(gamemap))
            maploader.close()
            rendermap()
        except:
            print("Error while saving map")
    if commandbar.get().startswith("!placeitem"):
        if commandbar.get()[11:] == "woodbarrier":
            if "woodbarrier" in playerinv:
                if playerinv["woodbarrier"] > 0:
                    gamemap[playerposy][playerposx] = {"blocktype":"woodbarrier","blockcolor":(218, 68, 61)}
                    setblock({"x":playerposx,"y":playerposy},(218, 68, 61))
                    playermove((playerposx, playerposy),(playerposx, playerposy))
                    playerinv["woodbarrier"] = playerinv["woodbarrier"] - 1
    if commandbar.get().startswith("!craftitem"):
        if commandbar.get()[11:] == "woodbarrier":
            if "wood" in playerinv:
                if playerinv["wood"] > 4:
                    playerinv["wood"] = playerinv["wood"] - 5
                    if not "woodbarrier" in playerinv:
                        playerinv["woodbarrier"] = 0
                    playerinv["woodbarrier"] = playerinv["woodbarrier"] + 2
                    print("woodbarrier crafted!")
                    print(playerinv)
                else:
                    print("You don't have 5 woods")
            else:
                print("you didn't get wood!")
    if commandbar.get().startswith("!getmap"):
        urltoget = commandbar.get()[8:]
        print("Getting map from URL")
        urlcontent = requests.get(commandbar.get()[8:]).content
        urlcontent = eval(urlcontent)
        #print(urlcontent)
        gamemap = urlcontent
        print("Got the map")
        rendermap()
    if commandbar.get().startswith("!pyexec"):
        exec(commandbar.get()[8:])
        

commandbar.bind('<Return>', docommand)

commandbar.grid(row=1, column=0)
                
#threading.Thread(target=gameloop).start()

print("b")

root.after(1, gameloop)

root.mainloop()