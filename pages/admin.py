import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv

class Admin:
    def __init__(self, main, args = {}):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Label(self.frame, text="Weclome, {} {}!".format(args.get("first_name"), args.get("last_name")), bg="skyblue").place(x=20, y=20)

        tk.Label(self.frame, text="Golf Cart Plate Number:", bg="skyblue").place(x=50, y=120)
        self.golf_cart_plate_num = tk.StringVar()
        tk.Entry(self.frame, width=30, textvariable=self.golf_cart_plate_num).place(x=220, y=120)

        tk.Label(self.frame, text="College:", bg="skyblue").place(x=80, y=155)
        self.college = tk.StringVar(value=self.main.colleges[0])
        self.cb = ttk.Combobox(self.frame, width=40, textvariable=self.college, values=self.main.colleges, state="readonly").place(x=180, y=155)

        tk.Button(self.frame, text="Create", width=10, command=self.create).place(x=220, y=220)

        tk.Label(self.frame, text="Create a backup for all golf carts", bg="skyblue").place(x=120, y=280)
        tk.Button(self.frame, text="Backup", width=10, command=self.backup).place(x=310, y=277)

        tk.Button(self.frame, text="Logout", width=10, command=self.logout).place(x=220, y=340)

    def create(self):
        conn = sqlite3.connect("ksu_golf_carts.db")
        golf_cart = list(conn.execute("SELECT * FROM golf_carts WHERE plate_number=" + self.golf_cart_plate_num.get()))
        if not golf_cart:
            if not self.college.get() in self.main.colleges:
                return messagebox.showerror(title="Wrong Input", message="The college is not exsits.")
            query = "INSERT INTO golf_carts (plate_number, college) VALUES (?,?)"
            data = (self.golf_cart_plate_num.get(), self.college.get())
            conn.execute(query, data)
            conn.commit()

            messagebox.showinfo(title="Golf Cart Created Successfully", message="The golf cart with plate number '{}' in '{}' college created successfully.".format(self.golf_cart_plate_num.get(), self.college.get()))

            self.golf_cart_plate_num.set("")
            self.college.set("")
        else:
            messagebox.showerror(title="Golf Cart Already Exists.", message="The golf cart with plate number '{}' already exists in '{}' college.".format(golf_cart[0][0], golf_cart[0][1]))
    
    def backup(self):
        conn = sqlite3.connect("ksu_golf_carts.db")
        golf_carts = list(conn.execute("SELECT * FROM golf_carts"))
        with open("golf_carts_backup.csv", "w") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerows(golf_carts)
        messagebox.showinfo(title="Backup Created Successfully", message="Stored {} golf carts.".format(len(golf_carts)))

    def logout(self):
        self.main.change_page("signup")