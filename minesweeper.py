# Python Version 2.7.3
# File: minesweeper.py

from Tkinter import *
import tkMessageBox
import random
import sys

class Minesweeper:

    def __init__(self, master):

        # import images
        self.tile_plain = PhotoImage(file = "images/tile_plain.gif")
        self.tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
        self.tile_mine = PhotoImage(file = "images/tile_mine.gif")
        self.tile_flag = PhotoImage(file = "images/tile_flag.gif")
        self.tile_wrong = PhotoImage(file = "images/tile_wrong.gif")

        # set up frame
        frame = Frame(master)
        frame.pack()

        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = 10)

        # create buttons
        self.buttons = dict({})
        mines = 0
        for x in range(0, 100):
            mine = 0
            ### gfx reassignable for debugging purposes
            gfx = self.tile_plain
            # currently random amount of mines
            if random.uniform(0.0, 1.0) < 0.1:
                mine = 1
                mines += 1
            # 0 = Button
            # 1 = if a mine y/n (1/0)
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
            self.buttons[x] = [ Button(frame, image = gfx), mine, 0 ]
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))
        
        # lay buttons in grid
        x = 1
        y = 0
        for key in self.buttons:
            self.buttons[key][0].grid( row = x, column = y )
            y += 1
            if y == 10:
                y = 0
                x += 1

        #add mine count at the end
        self.label2 = Label(frame, text="Mines: "+str(mines))
        self.label2.grid(row = 11, column = 0, columnspan = 10)

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(self.buttons[x])

    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(self.buttons[x])

    def lclicked(self, button_data):
        if button_data[1] == 1: #if a mine
            # show all mines and check for flags
            for key in self.buttons:
                if self.buttons[key][1] != 1 and self.buttons[key][2] == 2:
                    self.buttons[key][0].config(image = self.tile_wrong)
                if self.buttons[key][1] == 1 and self.buttons[key][2] != 2:
                    self.buttons[key][0].config(image = self.tile_mine)
                    
            # end game
            self.gameover()
        else:
            #change image and state
            button_data[0].config(image = self.tile_clicked)
            button_data[2] = 1

    def rclicked(self, button_data):
        # if not clicked
        if button_data[2] == 0:
            button_data[0].config(image = self.tile_flag)
            button_data[2] = 2

    def gameover(self):
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

### END OF CLASSES ###

root = Tk()

root.title("Minesweeper")

minesweeper = Minesweeper(root)

root.mainloop()
