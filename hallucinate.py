#!/usr/bin/env python3

#tesseraction net
#copyright - clayton thomas baber 2019

from tkinter import *
import time
import random
import torch
import numpy as np
import tkinter as tk
from tkinter import filedialog

color_state = ["#333333","red","orange","yellow","green","blue","cyan","purple","#ffffff"]

cHeight=600
cellSize=cHeight/28

tk = Tk()
tk.title("tesseraction.net")
tk.aspect(1,1,1,1)
canvas = Canvas(tk, width=cHeight, height=cHeight, bg="#424242")
canvas.pack(fill=BOTH, expand=1)


#all positions are relative to a 32x30 grid on the canvas
#first 0:15 pairs represent board posistions. 15:22 player one starting positions, 22:29 player two.
positions = (14,1),(9,4),(19,4),(14,7),(9,10),(19,10),(4,13),(14,13),(24,13),(9,16),(19,16),(14,19),(9,22),(19,22),(14,25),(4,4),(3,7),(2,10),(1,13),(2,16),(3,19),(4,22),(24,4),(25,7),(26,10),(27,13),(26,16),(25,19),(24,22)

#lines connecting board positions
lines = (0,1),(0,2),(0,4),(0,5),(1,6),(1,7),(1,3),(2,3),(2,7),(2,8),(3,9),(3,10),(4,6),(4,7),(4,11),(5,7),(5,8),(5,11),(6,12),(6,9),(7,9),(7,10),(7,12),(7,13),(8,10),(8,13),(9,14),(10,14),(11,12),(11,13),(12,14),(13,14)

#index here represents a board position, the value represent board positions that are neighbors
neighbors = (1,2,4,5),(0,3,6,7),(0,3,7,8),(1,2,9,10),(0,6,7,11),(0,7,8,11),(1,4,9,12),(1,2,4,5,9,10,12,13),(2,5,10,13),(3,6,7,14),(3,7,8,14),(4,5,12,13),(6,7,11,14),(7,8,11,14),(9,10,12,13)

t_space = [0,0,0,1,4,6,0,2,0,7,5,3,0,0,0]


gamestate = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,-1,1,0,0,1,1,1,0,0,1,-1,0,1,1,1,-1,0,1,0,0,0,-1,-1,-1,0,-1,-1,-1,1,-1,0,0,-1,-1,-1,0,0,-1,1,0,-1,-1,-1,1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#this contains all pertinent drawing locations for board stuff (positions, lines)
#should be recalculated each time the playing surface changes size
pixels = [(0,0,0,0)] * 75

def calculate_pixels(event):
    global cHeight, cellSize
    cHeight=min(event.width, event.height)
    cellSize = cHeight / 29

    #positions
    for i in range(29):
        pixels[i] = (positions[i][0]*cellSize+cellSize/4, positions[i][1]*cellSize+cellSize/4, (positions[i][0]+1)*cellSize-cellSize/4, (positions[i][1]+1)*cellSize-cellSize/4)

    #lines
    for i in range(32):
        pixels[i+29] = (positions[lines[i][0]][0]*cellSize+(cellSize/2), positions[lines[i][0]][1]*cellSize+(cellSize/2),positions[lines[i][1]][0]*cellSize+(cellSize/2), positions[lines[i][1]][1]*cellSize+(cellSize/2))

    #misc
    pixels[74] = cellSize/4, cellSize/8, cellSize, cellSize/2

    draw()


#if we decide we dont want to update grafics, set drawing to False
#this shouldn't prevent the game from running, just updating the view
drawing = True


def draw_t_space(posx, posy, transformer):
    if transformer == 0:
        return
    
    number = cellSize/2
    number2 = cellSize/3
    number3 = cellSize/2.5
    number4 = cellSize/12
    number5 = cellSize/4
    
    if transformer == 1:
        canvas.create_arc(posx - number3, posy - number3, posx + number3, posy + number3, start=0, extent=-180, width=number4, style=ARC)
    elif transformer == 2:
        canvas.create_arc(posx - number5, posy, posx + number5 + 3, posy + number5*2, start=90, extent=180, width=number4, style=ARC)
        canvas.create_arc(posx - number5, posy - number5*2, posx + number5, posy, start=90, extent=-180, width=number4, style=ARC)
    elif transformer == 3:
        canvas.create_arc(posx - number3, posy - number3, posx + number3, posy + number3, start=0, extent=180, width=number4, style=ARC)
    elif transformer == 4:
       canvas.create_line(posx, posy - number, posx, posy + number, width=number4)
    elif transformer == 5:
        canvas.create_line(posx - number, posy, posx + number, posy, width=number4)
    elif transformer == 6:
        canvas.create_line(posx - number2, posy + number2, posx + number2, posy - number2, width=number4)
    elif transformer == 7:
        canvas.create_line(posx - number2, posy - number2, posx + number2, posy + number2, width=number4)
    

def draw_st(posx, posy, state):
    color = color_state[4+sum(state)]
    number = cellSize/2
    number2 = number * 1.75
    number3 = number / 4
    number4 = number/6
    canvas.create_rectangle(posx - number, posy - number,posx + number, posy + number,  fill=color, outline="black", width=number4)
    
    #draw the four statelettes
    if state[0] != 0:
        if state[0] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx - number2, posy - number2,posx - number3, posy - number3, fill=color, width=number4)
    if state[1] != 0:
        if state[1] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx + number3, posy - number2,posx + number2, posy - number3, fill=color, width=number4)

    if state[2] != 0:
        if state[2] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx - number2, posy + number2,posx - number3, posy + number3, fill=color, width=number4)

    if state[3] != 0:
        if state[3] == 1:
            color = "white"
        else:
            color = color_state[0]
        canvas.create_oval(posx + number3, posy + number2,posx + number2, posy + number3, fill=color, width=number4)


#this function will draw the current gamestate on the canvas.
def draw():

    if not drawing: return
    
    #wipe the canvas clean
    canvas.delete(ALL)

    color = "#adadad"

   #draw the connecting lines
    for i in pixels[29:61]:
        canvas.create_line(i[0], i[1], i[2], i[3], fill=color, width=pixels[74][0])

    #draw each of the board positions
    for i,p in enumerate(pixels[:15]):
        canvas.create_oval(p[0], p[1], p[2], p[3], outline=color, fill=color, width=pixels[74][2])
        draw_t_space(p[0]+pixels[74][0], p[1]+pixels[74][0], t_space[i])


    #haxxx --- data tidying for compatibility reasons
    turn = gamestate[0]    

    #black magic... turn the simple list form into 4 component tuples
    occupations = list(zip(*[iter(gamestate[3:119])] * 4))

    selected = gamestate[119:148]


    #draw a player piece on the position it is occupying
    for i in range(29):
        if occupations[i] != (0,0,0,0):
            draw_st(pixels[i][0]+pixels[74][0], pixels[i][1]+pixels[74][0], occupations[i])
    
    if 1 in selected:
        if turn == 1:
            color = "white"
        else:
            color = "black"
        for selected_position in [i for i, x in enumerate(selected) if x == 1]:
            canvas.create_oval(pixels[selected_position][0]-pixels[74][2], pixels[selected_position][1]-pixels[74][2], pixels[selected_position][2]+pixels[74][2], pixels[selected_position][3]+pixels[74][2], outline=color, width=pixels[74][1])
    #update the canvas holder
    tk.update()
    
    #maybe slow down the animation to a visually pleasing speed
    #time.sleep(.1)
################################

def click(event):
    #loop through the positions and see if mouse click was on a board position
    for i in range(0, 29):
        if event.x > pixels[i][0]-pixels[74][0] and event.x < pixels[i][2]+pixels[74][0] and event.y > pixels[i][1]-pixels[74][0] and event.y < pixels[i][3]+pixels[74][0]:
            #clicked registered on the i'th position, process it
            action = [0] * 29
            action[i] = 1            
            clicked(action)
            break

def clicked(action):
    global gamestate

    #imagine a difference
    requested_reality = gamestate + action

    #change the world
    gamestate = np.round(model(torch.tensor(np.array(requested_reality, dtype=np.float32))).detach().numpy()).astype(np.int32).tolist()

    #we've made changes to the gamestate, so lets update board view
    draw()
    

#
#this will set the gamestate back to start
def right_click(event):
    clear_board()
    
def clear_board():
    global gamestate
    gamestate[:] = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,-1,1,0,0,1,1,1,0,0,1,-1,0,1,1,1,-1,0,1,0,0,0,-1,-1,-1,0,-1,-1,-1,1,-1,0,0,-1,-1,-1,0,0,-1,1,0,-1,-1,-1,1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    draw()

#fire click when left click
canvas.bind("<Button-1>", click)
#fire clear_board when right click
canvas.bind("<Button-3>", right_click)

#we need to recalculate the pixels list anytime the window is resized
tk.bind("<Configure>", calculate_pixels)
################################

#initialize board
draw()


rules_model_path = filedialog.askopenfilename()
model = torch.load(rules_model_path, map_location='cpu')



#so the window stays open, waiting for clickput
tk.mainloop()
