import tkinter as tk

class Login:
    def __init__(self, main):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Button(self.frame, text="Sign Up", width=10, command=self.signup).grid()

    def signup(self):
        self.main.change_page("signup")