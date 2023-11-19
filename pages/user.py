import tkinter as tk
from tkinter import ttk

class User:
    def __init__(self, main, args = {}):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.place(x=0, y=0)
        self.labelframe = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)
        self.labelframe2 = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        self.notebook.add(self.labelframe, text="Reserve a Cart")
        self.notebook.add(self.labelframe2, text="View my Reservations")