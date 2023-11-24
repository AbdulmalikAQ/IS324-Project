import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import sqlite3

class Login:
    def __init__(self, main, args = {}):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Label(self.frame, text="Welcome to our Application!", bg="skyblue", font=("Arial", 18, "bold")).place(x=85, y=60)

        tk.Label(self.frame, text="ID:", bg="skyblue").place(x=100, y=155)
        self.id = tk.StringVar()
        ttk.Entry(self.frame, width=30, textvariable=self.id).place(x=200, y=155)

        tk.Label(self.frame, text="Password:", bg="skyblue").place(x=100, y=190)
        self.password = tk.StringVar()
        ttk.Entry(self.frame, width=30, textvariable=self.password).place(x=200, y=190)

        ttk.Button(self.frame, text="Login", command=self.login).place(x=220, y=260)

        tk.Label(self.frame, text="Don't have an account?", bg="skyblue").place(x=135, y=330)
        ttk.Button(self.frame, text="Sign Up", command=self.signup).place(x=295, y=325)

    def login(self):
        if not self.id.get().isdigit():
            return messagebox.showerror(title="Wrong Data", message="ID must be digits only.")

        if len(self.password.get()) < 6:
            return messagebox.showerror(title="Wrong Data", message="Password must be at least 6 digits or letters")
        
        enteredPass = hashlib.sha256(self.password.get().encode()).hexdigest()
        conn = sqlite3.connect("ksu_golf_carts.db")
        userData = list(conn.execute("SELECT first_name, last_name, user_class, password FROM users WHERE user_id=" + self.id.get()))
        conn.close()
        if not userData or userData[0][3] != enteredPass:
            messagebox.showerror(title="Wrong User ID or Password", message="The entered user id or password is not valid.")
        else:
            if userData[0][2] == "Admin":
                self.main.change_page("admin", {"first_name": userData[0][0], "last_name": userData[0][1]})
            else:
                self.main.change_page("user", {"first_name": userData[0][0], "last_name": userData[0][1], "userClass":userData[0][2],"userID":self.id.get()})

    def signup(self):
        self.main.change_page("signup")