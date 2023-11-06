import tkinter as tk

class SignUp:
    def __init__(self, main):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Button(self.frame, text="Login", width=10, command=self.login).grid()

    def login(self):
        self.main.change_page("login")