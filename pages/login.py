import tkinter as tk
from tkinter import messagebox as ms
import hashlib
import sqlite3

class Login:
    def __init__(self, main):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Label(self.frame, text="ID:", bg="skyblue").place(x=100, y=120)
        self.id = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.id).place(x=200, y=120)

        tk.Label(self.frame, text="Password:", bg="skyblue").place(x=100, y=155)
        self.password = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.password).place(x=200, y=155)

        tk.Button(self.frame, text="Submit", width=10, command=self.submit).place(x=220, y=250)

        tk.Label(self.frame, text="Don't have an account?", bg="skyblue").place(x=135, y=320)
        tk.Button(self.frame, text="Sign Up", width=10, command=self.signup).place(x=295, y=317)

    def submit(self):
        conn = sqlite3.connect("ksu_golf_carts.db")
        passHashed = hashlib.sha256(self.password.get().encode()).hexdigest()
        ff = conn.execute("SELECT password from users where user_id=" + self.id.get())
        ff = list(ff)
        if ff[0][0] == passHashed:
            tk.messagebox.showinfo("data accepted", "Thanks for loging in!")
        else:
            tk.messagebox.showerror(title="Wrong Password", message="The password you entered is incorrect")
    def signup(self):
        self.main.change_page("signup")