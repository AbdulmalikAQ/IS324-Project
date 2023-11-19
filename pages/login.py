import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3

class Login:
    def __init__(self, main, args = {}):
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
<<<<<<< HEAD
        enteredPass = hashlib.sha256(self.password.get().encode()).hexdigest()
        conn = sqlite3.connect("ksu_golf_carts.db")
        userData = list(conn.execute("SELECT first_name, last_name, user_class, password FROM users WHERE user_id=" + self.id.get()))
        conn.close()
        if not userData or userData[0][3] != enteredPass:
            messagebox.showerror(title="Wrong User ID or Password", message="The entered user id or password is not valid.")
=======
        self.main.change_page("userwindow")

        conn = sqlite3.connect("ksu_golf_carts.db")
        passHashed = hashlib.sha256(self.password.get().encode()).hexdigest()
        ff = conn.execute("SELECT password from users where user_id=" + self.id.get())
        ff = list(ff)
        if len(ff)==0:
            tk.messagebox.showerror(title="Wrong ID", message="The ID you entered is incorrect")
        elif ff[0][0] == passHashed:
            self.main.change_page("userwindow")
>>>>>>> 01d68b088f0f0c55945a677f27f98579e40a207f
        else:
            if userData[0][2] == "Admin":
                self.main.change_page("admin", {"first_name": userData[0][0], "last_name": userData[0][1]})
            else:
                self.main.change_page("user", {"first_name": userData[0][0], "last_name": userData[0][1]})

    def signup(self):
        self.main.change_page("signup")