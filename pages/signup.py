import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

class SignUp:
    def __init__(self, main):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Label(self.frame, text="First Name:", bg="skyblue").place(x=75, y=50)
        self.first_name = tk.StringVar()
        tk.Entry(self.frame, width=15, textvariable=self.first_name).place(x=145, y=50)

        tk.Label(self.frame, text="Last Name:", bg="skyblue").place(x=255, y=50)
        self.last_name = tk.StringVar()
        tk.Entry(self.frame, width=15, textvariable=self.last_name).place(x=325, y=50)

        tk.Label(self.frame, text="ID:", bg="skyblue").place(x=100, y=90)
        self.id = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.id).place(x=200, y=90)

        tk.Label(self.frame, text="Password:", bg="skyblue").place(x=100, y=130)
        self.Password = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.Password).place(x=200, y=130)

        tk.Label(self.frame, text="Email address:", bg="skyblue").place(x=100, y=170)
        self.EmailAddress = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.EmailAddress).place(x=200, y=170)

        tk.Label(self.frame, text="Phone number:", bg="skyblue").place(x=100, y=210)
        self.phoneNumber = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.phoneNumber).place(x=200, y=210)

        tk.Label(self.frame, text="User Class:", bg="skyblue").place(x=100, y=250)
        self.team = tk.IntVar(value=0)
        self.teams = ("Student", "Faculty", "Employee")
        tk.Radiobutton(self.frame, text=self.teams[0], variable=self.team, value=0, bg="skyblue").place(x=180, y=250)
        tk.Radiobutton(self.frame, text=self.teams[1], variable=self.team, value=1, bg="skyblue").place(x=260, y=250)
        tk.Radiobutton(self.frame, text=self.teams[2], variable=self.team, value=2, bg="skyblue").place(x=330, y=250)

        tk.Button(self.frame, text="Submit", width=10, command=self.submit).place(x=220, y=300)

        tk.Label(self.frame, text="Already have an account?", bg="skyblue").place(x=135, y=350)
        tk.Button(self.frame, text="Login", width=10, command=self.login).place(x=295, y=347)

    def submit(self):
        messagebox.showerror(title="Not available yet", message="Wait for the next version")

    def login(self):
        self.main.change_page("login")
