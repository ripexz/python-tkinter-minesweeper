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
        self.tile_no = []
        for x in range(1, 9):
            self.tile_no.append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

        # set up frame
        frame = Frame(master)
        frame.pack()

        # show "Minesweeper" at the top
        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = 10)

        # create buttons
        self.buttons = dict({})
        mines = 0
        x_coord = 1
        y_coord = 0
        for x in range(0, 100):
            mine = 0
            # tile image changeable for debug reasons:
            gfx = self.tile_plain
            # currently random amount of mines
            if random.uniform(0.0, 1.0) < 0.1:
                mine = 1
                mines += 1
            # 0 = Button
            # 1 = if a mine y/n (1/0)
            # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
            # 3 = button id
            # 4 = [x, y] coordinates in the grid
            # 5 = nearby mines, 0 by default, calculated after placement in grid
            self.buttons[x] = [ Button(frame, image = gfx),
                                mine,
                                0,
                                x,
                                [x_coord, y_coord],
                                0 ]
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))

            # calculate coords:
            y_coord += 1
            if y_coord == 10:
                y_coord = 0
                x_coord += 1
        
        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key][0].grid( row = self.buttons[key][4][0], column = self.buttons[key][4][1] )

        # find nearby mines and display number on tile
        for key in self.buttons:
            nearby_mines = 0
            # if not at edges
            if self.buttons[key][4][0] != 1 and self.buttons[key][4][0] != 10 \
            and self.buttons[key][4][1] != 0 and self.buttons[key][4][1] != 9:
                if self.buttons[key-9][1] == 1:     #top right
                    nearby_mines += 1
                if self.buttons[key-10][1] == 1:    #top middle
                    nearby_mines += 1
                if self.buttons[key-11][1] == 1:    #top left
                    nearby_mines += 1
                if self.buttons[key-1][1] == 1:     #left
                    nearby_mines += 1
                if self.buttons[key+1][1] == 1:     #right
                    nearby_mines += 1
                if self.buttons[key+9][1] == 1:     #bottom left
                    nearby_mines += 1
                if self.buttons[key+10][1] == 1:    #bottom middle
                    nearby_mines += 1
                if self.buttons[key+11][1] == 1:    #bottom right
                    nearby_mines += 1

            # if top row:
            if self.buttons[key][4][0] == 1:
                if self.buttons[key+10][1] == 1:    #bottom middle
                    nearby_mines += 1
                # if not top left
                if self.buttons[key][4][1] != 0:
                    if self.buttons[key-1][1] == 1:     #left
                        nearby_mines += 1
                    if self.buttons[key+9][1] == 1:     #bottom left
                        nearby_mines += 1
                # if not top right
                if self.buttons[key][4][1] != 9:
                    if self.buttons[key+1][1] == 1:     #right
                        nearby_mines += 1
                    if self.buttons[key+11][1] == 1:    #bottom right
                        nearby_mines += 1
            # if bottom row:
            if self.buttons[key][4][0] == 10:
                if self.buttons[key-10][1] == 1:    #top middle
                    nearby_mines += 1
                # if not bottom left
                if self.buttons[key][4][1] != 0:
                    if self.buttons[key-1][1] == 1:     #left
                        nearby_mines += 1
                    if self.buttons[key-11][1] == 1:    #top left
                        nearby_mines += 1
                # if not top right
                if self.buttons[key][4][1] != 9:
                    if self.buttons[key+1][1] == 1:     #right
                        nearby_mines += 1
                    if self.buttons[key-9][1] == 1:     #top right
                        nearby_mines += 1
            # if left side but not top or bottom:
            if self.buttons[key][4][1] == 0 and self.buttons[key][4][0] != 1 \
                                            and self.buttons[key][4][0] != 10:
                if self.buttons[key-10][1] == 1:    #top middle
                    nearby_mines += 1
                if self.buttons[key-9][1] == 1:     #top right
                    nearby_mines += 1
                if self.buttons[key+1][1] == 1:     #right
                    nearby_mines += 1
                if self.buttons[key+11][1] == 1:    #bottom right
                    nearby_mines += 1
                if self.buttons[key+10][1] == 1:    #bottom middle
                    nearby_mines += 1
            # if right side but not top or bottom:
            if self.buttons[key][4][1] == 9 and self.buttons[key][4][0] != 1 \
                                            and self.buttons[key][4][0] != 10:
                if self.buttons[key-10][1] == 1:    #top middle
                    nearby_mines += 1
                if self.buttons[key-11][1] == 1:    #top left
                    nearby_mines += 1
                if self.buttons[key-1][1] == 1:     #left
                    nearby_mines += 1
                if self.buttons[key+9][1] == 1:     #bottom left
                    nearby_mines += 1
                if self.buttons[key+10][1] == 1:    #bottom middle
                    nearby_mines += 1

            # store mine count in button data list
            self.buttons[key][5] = nearby_mines

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
            if button_data[5] == 0:
                button_data[0].config(image = self.tile_clicked)
            else:
                button_data[0].config(image = self.tile_no[button_data[5]-1])
            button_data[2] = 1

    def rclicked(self, button_data):
        # if not clicked
        if button_data[2] == 0:
            button_data[0].config(image = self.tile_flag)
            button_data[2] = 2
            button_data[0].unbind('<Button-1>')
        # if flagged, unflag
        elif button_data[2] == 2:
            button_data[0].config(image = self.tile_plain)
            button_data[2] = 0
            button_data[0].bind('<Button-1>', self.lclicked_wrapper(button_data[3]))

    def gameover(self):
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

### END OF CLASSES ###

# create Tk widget
root = Tk()
# set program title
root.title("Minesweeper")
# create game instance
minesweeper = Minesweeper(root)
# run event loop
root.mainloop()
