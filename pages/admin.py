import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv

class Admin:
    def __init__(self, main, args = {}):
        self.main = main
        self.main.window.title("KSU Golf Carts - Admin Panel")
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        tk.Label(self.frame, text="Welcome, {} {}!".format(args.get("first_name"), args.get("last_name")), bg="skyblue", font=("Arial", 10, "bold")).place(x=20, y=20)

        tk.Label(self.frame, text="Insert New Golf Cart", bg="skyblue", font=("Arial", 18, "bold")).place(x=135, y=80)

        tk.Label(self.frame, text="Plate Number:", bg="skyblue").place(x=80, y=160)
        self.plate_number = tk.StringVar()
        ttk.Entry(self.frame, width=30, textvariable=self.plate_number).place(x=180, y=160)

        tk.Label(self.frame, text="College:", bg="skyblue").place(x=80, y=195)
        self.college = tk.StringVar(value=self.main.constants.get("colleges")[0])
        self.cb = ttk.Combobox(self.frame, width=40, textvariable=self.college, values=self.main.constants.get("colleges"), state="readonly").place(x=180, y=195)

        ttk.Button(self.frame, text="Create", width=10, command=self.create).place(x=220, y=260)

        tk.Label(self.frame, text="Create a backup for all golf carts", bg="skyblue").place(x=120, y=320)
        ttk.Button(self.frame, text="Backup", width=10, command=self.backup).place(x=310, y=315)

        ttk.Button(self.frame, text="Logout", width=10, command=self.logout).place(x=415, y=360)

    def create(self):
        if not self.plate_number.get():
            return messagebox.showerror(title="Missing Data", message="You must enter a golf cart plate number.")
        
        conn = sqlite3.connect("ksu_golf_carts.db")
        golf_cart = list(conn.execute("SELECT * FROM golf_carts WHERE plate_number=" + self.plate_number.get()))
        if not golf_cart:
            if not self.college.get() in self.main.constants.get("colleges"):
                return messagebox.showerror(title="Wrong Input", message="The college is not exsits.")
            query = "INSERT INTO golf_carts (plate_number, college) VALUES (?,?)"
            data = (self.plate_number.get(), self.college.get())
            conn.execute(query, data)
            conn.commit()

            messagebox.showinfo(title="Golf Cart Inserted Successfully", message="The golf cart with plate number '{}' in '{}' college inserted successfully.".format(self.plate_number.get(), self.college.get()))

            self.plate_number.set("")
            self.college.set(self.main.constants.get("colleges")[0])
        else:
            messagebox.showerror(title="Golf Cart Already Exists.", message="The golf cart with plate number '{}' already exists in '{}' college.".format(golf_cart[0][0], golf_cart[0][1]))
    
    def backup(self):
        conn = sqlite3.connect("ksu_golf_carts.db")
        golf_carts = list(conn.execute("SELECT * FROM golf_carts"))
        reservations = list(conn.execute("SELECT * FROM reservations"))
        users = list(conn.execute("SELECT * FROM users"))
        conn.close()
        with open("backup/golf_carts.csv", "w") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerows(golf_carts)
        with open("backup/reservations.csv", "w") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerows(reservations)
        with open("backup/users.csv", "w") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerows(users)
        messagebox.showinfo(title="Backup Created Successfully", message="Backup created, stored {} golf carts, {} reservations and {} users.".format(len(golf_carts), len(reservations), len(users)))

    def logout(self):
        self.main.change_page("signup")