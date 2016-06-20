#!/usr/bin/python


import itertools
import sys
import time
import Tkinter
import tkSimpleDialog
import tkMessageBox
from Tkinter import *


def dosomething():
    print "hej"

if __name__ == "__main__":
    # Inputdialog
    root = Tkinter.Tk()
    # root.wm_deiconify()

    frame = Frame(root, width=100, height=100)
    frame.bind("<Button-1>", )
    frame.pack()

    root.mainloop()
    # root.withdraw()
    # tkMessageBox.showinfo("info")
    # tkMessageBox.showerror("error")
    # tkMessageBox.showwarning("warning")

