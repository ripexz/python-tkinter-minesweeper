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

        # set up frame
        frame = Frame(master)
        frame.pack()

        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = 10)

        # create buttons
        self.buttons = dict({})
        for x in range(0, 100):
            mine = 0
            gfx = self.tile_plain
            if random.uniform(0.0, 1.0) < 0.2:
                mine = 1
                gfx = self.tile_mine
            self.buttons[x] = [ Button(frame, image = gfx, command = self.clicked_factory(x)), mine ]
        
        # lay buttons in grid
        x = 1
        y = 0
        for key in self.buttons:
            self.buttons[key][0].grid( row = x, column = y )
            y += 1
            if y == 10:
                y = 0
                x += 1

    def clicked_factory(self, x):
        return lambda: self.clicked(self.buttons[x])

    def clicked(self, button_data):
        if button_data[1] == 1: #if a mine
            self.gameover()
        else:
            button_data[0].config( image = self.tile_clicked )

    def gameover(self):
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

### END OF CLASSES ###

root = Tk()

root.title("Minesweeper")

minesweeper = Minesweeper(root)

root.mainloop()
