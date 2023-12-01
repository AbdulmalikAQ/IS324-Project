import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3
import logging

logging.basicConfig(filename="transactions.log", filemode="a", format="%(asctime)s - %(message)s", level=logging.INFO)

class User:
    def __init__(self, main, args = {}):
        self.main = main
        self.main.window.title("KSU Golf Carts - User Panel")
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        self.args = args

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.place(x=0, y=0)

        tk.Label(self.frame, text="Welcome, {} {}!".format(self.args.get("first_name"), self.args.get("last_name")), bg="skyblue", font=("Arial", 10, "bold")).place(x=20, y=45)

        self.labelframe = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        tk.Label(self.labelframe, text="Reserve a Cart", bg="skyblue", font=("Arial", 18, "bold")).place(x=160, y=65)

        tk.Label(self.labelframe, text="College:", bg="skyblue").place(x=70, y=130)
        self.college = tk.StringVar(value=self.main.constants.get("colleges")[0])
        self.cb = ttk.Combobox(self.labelframe, width=40, textvariable=self.college, values=self.main.constants.get("colleges"), state="readonly").place(x=150, y=130)

        tk.Label(self.labelframe, text="Start date and time:", bg="skyblue").place(x=70, y=180)
        self.start_date = DateEntry(self.labelframe, date_pattern="dd/mm/y", state="readonly")
        self.start_date.place(x=200, y=180)
        time_now = datetime.now()
        self.start_hour = tk.StringVar(value=time_now.hour)
        tk.Spinbox(self.labelframe, from_=0, to=23, wrap=True, width=3, state="readonly", textvariable=self.start_hour).place(x=300, y=180)
        self.start_min = tk.StringVar(value=time_now.minute)
        tk.Spinbox(self.labelframe, from_=0, to=59, wrap=True, width=3, state="readonly", textvariable=self.start_min).place(x=335, y=180)

        tk.Label(self.labelframe, text="End date and time:", bg="skyblue").place(x=70, y=220)
        self.end_date = DateEntry(self.labelframe, date_pattern="dd/mm/y", state="readonly")
        self.end_date.place(x=200, y=220)
        self.end_hour = tk.StringVar(value=time_now.hour)
        tk.Spinbox(self.labelframe, from_=0, to=23, wrap=True, width=3, state="readonly", textvariable=self.end_hour).place(x=300, y=220)
        self.end_min = tk.StringVar(value=time_now.minute)
        tk.Spinbox(self.labelframe, from_=0, to=59, wrap=True, width=3, state="readonly", textvariable=self.end_min).place(x=335, y=220)

        ttk.Button(self.labelframe, text="Reserve", command=self.reserve).place(x=220, y=285)

        self.labelframe2 = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        tk.Label(self.labelframe2, text="My Reservations", bg="skyblue", font=("Arial", 18, "bold")).place(x=150, y=60)

        self.tv_of_reserv = ttk.Treeview(self.labelframe2, height=7, columns=(1, 2, 3, 4), show="headings")
        self.tv_of_reserv.heading(1, text="Plate Number")
        self.tv_of_reserv.column(1, minwidth=0, width=100, anchor=tk.CENTER)
        self.tv_of_reserv.heading(2, text="Location")
        self.tv_of_reserv.column(2, minwidth=0, width=110, anchor=tk.CENTER)
        self.tv_of_reserv.heading(3, text="Start Time")
        self.tv_of_reserv.column(3, minwidth=0, width=120, anchor=tk.CENTER)
        self.tv_of_reserv.heading(4, text="End Time")
        self.tv_of_reserv.column(4, minwidth=0, width=120, anchor=tk.CENTER)
        self.tv_of_reserv.place(x=20, y=110)

        ttk.Button(self.labelframe2, text="Show", command=self.show).place(x=220, y=300)

        ttk.Button(self.frame, text="Logout", command=self.logout).place(x=405, y=360)

        self.notebook.add(self.labelframe, text="Reserve a Cart")
        self.notebook.add(self.labelframe2, text="View my Reservations")

    def reserve(self):
        start_time = datetime.strptime("{} {}:{}".format(self.start_date.get(), self.start_hour.get(), self.start_min.get()), "%d/%m/%Y %H:%M")
        end_time = datetime.strptime("{} {}:{}".format(self.end_date.get(), self.end_hour.get(), self.end_min.get()), "%d/%m/%Y %H:%M")
        date_now = datetime.now()
        if start_time < date_now:
            logging.warning("Start time precedes current time, User ID: {}, Location: NONE, Golf Cart Plate Number: NONE, Start Time: {}, End Time: {}".format(self.args.get("user_id"), start_time, end_time))
            return messagebox.showerror(title="Time Error", message="Start time must be after the current time.")
        reserve_time = end_time - start_time
        max_time = self.main.constants.get("user_max_time").get(self.args.get("user_class"))
        if reserve_time.total_seconds() <= 0:
            logging.warning("Start time precedes end time, User ID: {}, Location: NONE, Golf Cart Plate Number: NONE, Start Time: {}, End Time: {}".format(self.args.get("user_id"), start_time, end_time))
            return messagebox.showerror(title="Time Error", message="End time must be greater than the start time.")
        elif reserve_time.total_seconds() > max_time:
            logging.warning("Reserve time exceeds the time limit, User ID: {}, Location: NONE, Golf Cart Plate Number: NONE, Start Time: {}, End Time: {}".format(self.args.get("user_id"), start_time, end_time))
            return messagebox.showerror(title="Time Exceed", message="You can't reserve a golf cart longer than {} minutes.".format(max_time / 60))
        else:
            conn = sqlite3.connect("ksu_golf_carts.db")
            golf_cart_plates = list(conn.execute("SELECT plate_number FROM golf_carts WHERE college = ?", (self.college.get(),)))
            for (plate,) in golf_cart_plates:
                reserved_dates = list(conn.execute("SELECT start_time, end_time FROM reservations WHERE plate_number = ?", (plate,)))
                conflict = False
                for (reserved_start, reserved_end) in reserved_dates:
                    reserved_start = datetime.strptime(reserved_start, "%Y-%m-%d %H:%M:%S")
                    reserved_end = datetime.strptime(reserved_end, "%Y-%m-%d %H:%M:%S")
                    if (reserved_start <= start_time <= reserved_end) or (reserved_start <= end_time <= reserved_end) or (start_time < reserved_start and end_time > reserved_end):
                        conflict = True
                        break
                
                if not conflict:
                    query = "INSERT INTO reservations (plate_number, user_id, start_time, end_time) VALUES (?,?,?,?)"
                    data = (plate, self.args.get("user_id"), start_time, end_time)
                    conn.execute(query, data)
                    conn.commit()
                    conn.close()
                    logging.info("Reservation successful, User ID: {}, Location: {}, Golf Cart Plate Number: {}, Start Time: {}, End Time: {}".format(self.args.get("user_id"), self.college.get(), plate, start_time, end_time))
                    return messagebox.showinfo(title="Reservation Successful", message="You have reserved a golf cart with plate number '{}' from '{}' college at '{}' to '{}'".format(plate, self.college.get(), start_time, end_time))
            
            logging.warning("No golf carts available, User ID: {}, Location: NONE, Golf Cart Plate Number: NONE, Start Time: {}, End Time: {}".format(self.args.get("user_id"), start_time, end_time))
            messagebox.showerror(title="No Golf Carts Available", message="There is no golf carts available from this college at this time.")

    def show(self):
        self.tv_of_reserv.delete(*self.tv_of_reserv.get_children())
        conn = sqlite3.connect("ksu_golf_carts.db")
        reservations = list(conn.execute("SELECT reservations.plate_number, college, start_time, end_time FROM reservations JOIN golf_carts ON reservations.plate_number=golf_carts.plate_number WHERE user_id = ?", (self.args.get("user_id"),)))
        date_now = datetime.now()
        for reserv in reservations:
            reserved_end = datetime.strptime(reserv[3], "%Y-%m-%d %H:%M:%S")
            if reserved_end >= date_now:
                self.tv_of_reserv.insert(parent="", index=0, values=(reserv[0], reserv[1], datetime.strptime(reserv[2], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M"), reserved_end.strftime("%d/%m/%Y %H:%M")))

        if len(self.tv_of_reserv.get_children()) == 0:
            messagebox.showwarning(title="No Active Reservations", message="You don't have any active reservations at this moment.")

    def logout(self):
        self.main.change_page("signup")