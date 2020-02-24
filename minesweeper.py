# Python Version 2.7.3
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
import random
import platform
from collections import deque

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
        x_coord = 1
        y_coord = 0
        for x in range(0, 100):
            isMine = 0

            # tile image changeable for debug reasons:
            gfx = self.tiles["plain"]

            # currently random amount of mines
            if random.uniform(0.0, 1.0) < 0.1:
                isMine = 1
                self.mines += 1

            self.buttons[x] = {
                "id": x,
                "isMine": isMine,
                "state": STATE_DEFAULT,
                "coords": {
                    "x": x_coord,
                    "y": y_coord
                },
                "widget": Button(frame, image = gfx),
                "mines": 0 # calculated after placement in grid
            }

            self.buttons[x]["widget"].bind(BTN_CLICK, self.lclicked_wrapper(x))
            self.buttons[x]["widget"].bind(BTN_FLAG, self.rclicked_wrapper(x))

            # calculate coords for next loop:
            y_coord += 1
            if y_coord == 10:
                y_coord = 0
                x_coord += 1

        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key]["widget"].grid( row = self.buttons[key]["coords"]["x"], column = self.buttons[key]["coords"]["y"] )

        # find nearby mines and display number on tile
        for key in self.buttons:
            nearby_mines = 0
            if self.check_for_mines(key-9):
                nearby_mines += 1
            if self.check_for_mines(key-10):
                nearby_mines += 1
            if self.check_for_mines(key-11):
                nearby_mines += 1
            if self.check_for_mines(key-1):
                nearby_mines += 1
            if self.check_for_mines(key+1):
                nearby_mines += 1
            if self.check_for_mines(key+9):
                nearby_mines += 1
            if self.check_for_mines(key+10):
                nearby_mines += 1
            if self.check_for_mines(key+11):
                nearby_mines += 1
            # store mine count in button data list
            self.buttons[key]["mines"] = nearby_mines
            #if self.buttons[key]["isMine"] != 1:
            #    if nearby_mines != 0:
            #        self.buttons[key]["widget"].config(image = self.tiles["numbers"][nearby_mines-1])

        #add mine and count at the end
        self.label2 = Label(frame, text = "Mines: "+str(self.mines))
        self.label2.grid(row = 11, column = 0, columnspan = 5)

        self.label3 = Label(frame, text = "Flags: "+str(self.flags))
        self.label3.grid(row = 11, column = 4, columnspan = 5)

    ## End of __init__

    def check_for_mines(self, key):
        try:
            if self.buttons[key]["isMine"] == 1:
                return True
        except KeyError:
            pass

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(self.buttons[x])

    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(self.buttons[x])

    def lclicked(self, button_data):
        if button_data["isMine"] == 1:
            # show all mines and check for flags
            for key in self.buttons:
                if self.buttons[key]["isMine"] == 0 and self.buttons[key]["state"] == STATE_FLAGGED:
                    self.buttons[key]["widget"].config(image = self.tiles["wrong"])
                if self.buttons[key]["isMine"] == 1 and self.buttons[key]["state"] != STATE_FLAGGED:
                    self.buttons[key]["widget"].config(image = self.tiles["mine"])
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
            if button_data["isMine"] == 1:
                self.correct_flags += 1
            self.flags += 1
            self.update_flags()
        # if flagged, unflag
        elif button_data["state"] == 2:
            button_data["widget"].config(image = self.tiles["plain"])
            button_data["state"] = 0
            button_data["widget"].bind(BTN_CLICK, self.lclicked_wrapper(button_data["id"]))
            # if a mine
            if button_data["isMine"] == 1:
                self.correct_flags -= 1
            self.flags -= 1
            self.update_flags()

    def check_tile(self, key, queue):
        try:
            if self.buttons[key]["state"] == STATE_DEFAULT:
                if self.buttons[key]["mines"] == 0:
                    self.buttons[key]["widget"].config(image = self.tiles["clicked"])
                    queue.append(key)
                else:
                    self.buttons[key]["widget"].config(image = self.tiles["numbers"][self.buttons[key]["mines"]-1])
                self.buttons[key]["state"] = STATE_CLICKED
                self.clicked += 1
        except KeyError:
            pass

    def clear_empty_tiles(self, main_key):
        queue = deque([main_key])

        while len(queue) != 0:
            key = queue.popleft()
            self.check_tile(key-9, queue)      #top right
            self.check_tile(key-10, queue)     #top middle
            self.check_tile(key-11, queue)     #top left
            self.check_tile(key-1, queue)      #left
            self.check_tile(key+1, queue)      #right
            self.check_tile(key+9, queue)      #bottom right
            self.check_tile(key+10, queue)     #bottom middle
            self.check_tile(key+11, queue)     #bottom left

    def gameover(self):
        tkMessageBox.showinfo("Game Over", "You Lose!")
        global root
        root.destroy()

    def victory(self):
        tkMessageBox.showinfo("Game Over", "You Win!")
        global root
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
