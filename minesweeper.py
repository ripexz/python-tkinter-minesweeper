# Python Version 2.7.3
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time

SIZE_X = 10
SIZE_Y = 10

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

class Minesweeper:

    def __init__(self, master):

        # import images
        self.tiles = {
            "plain": PhotoImage(file = "images/tile_plain.gif"),
            "clicked": PhotoImage(file = "images/tile_clicked.gif"),
            "mine": PhotoImage(file = "images/tile_mine.gif"),
            "flag": PhotoImage(file = "images/tile_flag.gif"),
            "wrong": PhotoImage(file = "images/tile_wrong.gif"),
            "numbers": []
        }
        for x in range(1, 9):
            self.tiles["numbers"].append(PhotoImage(file = "images/tile_"+str(x)+".gif"))

        # set up frame
        frame = Frame(master)
        frame.pack()

        # show "Minesweeper" at the top
        self.label1 = Label(frame, text="Minesweeper")
        self.label1.grid(row = 0, column = 0, columnspan = 10)

        # create flag and clicked tile variables
        self.flags = 0
        self.correct_flags = 0
        self.clicked = 0

        # create buttons
        self.buttons = dict({})
        self.mines = 0
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if y == 0:
                    self.buttons[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # tile image changeable for debug reasons:
                gfx = self.tiles["plain"]

                # currently random amount of mines
                if random.uniform(0.0, 1.0) < 0.1:
                    isMine = True
                    self.mines += 1

                self.buttons[x][y] = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "widget": Button(frame, image = gfx),
                    "mines": 0 # calculated after grid is built
                }

                self.buttons[x][y]["widget"].bind(BTN_CLICK, self.lclicked_wrapper(x, y))
                self.buttons[x][y]["widget"].bind(BTN_FLAG, self.rclicked_wrapper(x, y))

                # lay buttons in grid
                self.buttons[x][y]["widget"].grid( row = x, column = y )

        # loop again to find nearby mines and display number on tile
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                nearby_mines = 0
                nearby_mines += 1 if self.check_for_mines(x-1, y-1) else 0  #top right
                nearby_mines += 1 if self.check_for_mines(x-1, y) else 0    #top middle
                nearby_mines += 1 if self.check_for_mines(x-1, y+1) else 0  #top left
                nearby_mines += 1 if self.check_for_mines(x, y-1) else 0    #left
                nearby_mines += 1 if self.check_for_mines(x, y+1) else 0    #right
                nearby_mines += 1 if self.check_for_mines(x+1, y-1) else 0  #bottom right
                nearby_mines += 1 if self.check_for_mines(x+1, y) else 0    #bottom middle
                nearby_mines += 1 if self.check_for_mines(x+1, y+1) else 0  #bottom left

                self.buttons[x][y]["mines"] = nearby_mines

        #add mine and count at the end
        self.label2 = Label(frame, text = "Mines: "+str(self.mines))
        self.label2.grid(row = SIZE_X+1, column = 0, columnspan = SIZE_Y/2)

        self.label3 = Label(frame, text = "Flags: "+str(self.flags))
        self.label3.grid(row = SIZE_X+1, column = SIZE_Y/2-1, columnspan = SIZE_Y/2)

    ## End of __init__

    def check_for_mines(self, x, y):
        try:
            return self.buttons[x][y]["isMine"]
        except KeyError:
            pass

    def lclicked_wrapper(self, x, y):
        return lambda Button: self.lclicked(self.buttons[x][y])

    def rclicked_wrapper(self, x, y):
        return lambda Button: self.rclicked(self.buttons[x][y])

    def lclicked(self, button_data):
        if button_data["isMine"] == True:
            # end game
            self.gameover()
        else:
            # change image
            if button_data["mines"] == 0:
                button_data["widget"].config(image = self.tiles["clicked"])
                self.clear_empty_tiles(button_data["id"])
            else:
                button_data["widget"].config(image = self.tiles["numbers"][button_data["mines"]-1])
            # if not already set as clicked, change state and count
            if button_data["state"] != STATE_CLICKED:
                button_data["state"] = STATE_CLICKED
                self.clicked += 1
            if self.clicked == 100 - self.mines:
                self.victory()

    def rclicked(self, button_data):
        # if not clicked
        if button_data["state"] == STATE_DEFAULT:
            button_data["widget"].config(image = self.tiles["flag"])
            button_data["state"] = STATE_FLAGGED
            button_data["widget"].unbind(BTN_CLICK)
            # if a mine
            if button_data["isMine"] == True:
                self.correct_flags += 1
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif button_data["state"] == 2:
            button_data["widget"].config(image = self.tiles["plain"])
            button_data["state"] = 0
            button_data["widget"].bind(BTN_CLICK, self.lclicked_wrapper(button_data["coords"]["x"], button_data["coords"]["y"]))
            # if a mine
            if button_data["isMine"] == True:
                self.correct_flags -= 1
            self.flags -= 1
            self.update_flags()

    def check_tile(self, x, y, queue):
        try:
            if self.buttons[x][y]["state"] == STATE_DEFAULT:
                if self.buttons[x][y]["mines"] == 0:
                    self.buttons[x][y]["widget"].config(image = self.tiles["clicked"])
                    queue.append(self.buttons[x][y]["id"])
                else:
                    self.buttons[x][y]["widget"].config(image = self.tiles["numbers"][self.buttons[x][y]["mines"]-1])
                self.buttons[x][y]["state"] = STATE_CLICKED
                self.clicked += 1
        except KeyError:
            pass

    def clear_empty_tiles(self, id):
        queue = deque([id])

        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            source_x = int(parts[0])
            source_y = int(parts[1])

            self.check_tile(source_x-1, source_y-1, queue)  #top right
            self.check_tile(source_x-1, source_y, queue)    #top middle
            self.check_tile(source_x-1, source_y+1, queue)  #top left
            self.check_tile(source_x, source_y-1, queue)    #left
            self.check_tile(source_x, source_y+1, queue)    #right
            self.check_tile(source_x+1, source_y-1, queue)  #bottom right
            self.check_tile(source_x+1, source_y, queue)    #bottom middle
            self.check_tile(source_x+1, source_y+1, queue)  #bottom left

    def reveal(self):
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if self.buttons[x][y]["isMine"] == False and self.buttons[x][y]["state"] == STATE_FLAGGED:
                    self.buttons[x][y]["widget"].config(image = self.tiles["wrong"])
                if self.buttons[x][y]["isMine"] == True and self.buttons[x][y]["state"] != STATE_FLAGGED:
                    self.buttons[x][y]["widget"].config(image = self.tiles["mine"])
        global root
        root.update()

    def gameover(self):
        self.reveal()
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

    def victory(self):
        self.reveal()
        tkMessageBox.showinfo("Game Over", "You Win!")
        root.destroy()

    def update_flags(self):
        self.label3.config(text = "Flags: "+str(self.flags))

### END OF CLASSES ###

def main():
    global root
    # create Tk widget
    root = Tk()
    # set program title
    root.title("Minesweeper")
    # create game instance
    minesweeper = Minesweeper(root)
    # run event loop
    root.mainloop()

if __name__ == "__main__":
    main()
