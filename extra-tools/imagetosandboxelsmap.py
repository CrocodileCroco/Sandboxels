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

gfil = input("Filename of the image? (in the current directory) : ")
im = Image.open(gfil)
data = np.asarray(im)
print(data)
width, height = im.size
img = Image.new('RGB', (width, height), color = 'white')
pixels = img.load()
gamemap = []
for j in range(height):
    gamemap.append([])
    for i in range(width):
        gamemap[j].append({"blocktype":"grass","blockcolor":tuple(data[j,i])})
goutp = input("Output filename : ")
maploader = open(goutp, "w")
maploader.write(str(gamemap))
maploader.close()
