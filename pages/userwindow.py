import tkinter as tk
from tkinter import ttk

class UserWindow:
    def __init__(self, main):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.place(x=0,y=0)
        self.labelframe = tk.Frame(self.notebook, width=400,height=280)
        self.labelframe2 = tk.Frame(self.notebook, width=400,height=280)

        self.notebook.add(self.labelframe, text='Reserve a Cart')

        self.notebook.add(self.labelframe2, text='View my Reservations)')
