import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

class User:
    def __init__(self, main, args = {}):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.place(x=0, y=0)

        self.userID=args.get("userID")
        self.userClass=args.get("userClass")
        tk.Label(self.frame, text="Weclome, {} {}!".format(args.get("first_name"), args.get("last_name")), bg="skyblue", font=("Arial", 10, "bold")).place(x=20, y=45)

        self.labelframe = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        tk.Label(self.labelframe, text="Reserve a Cart", bg="skyblue", font=("Arial", 18, "bold")).place(x=160, y=60)

        tk.Label(self.labelframe, text="College:", bg="skyblue").place(x=70, y=130)
        self.college = tk.StringVar(value=self.main.colleges[0])
        self.cb = ttk.Combobox(self.labelframe, width=40, textvariable=self.college, values=self.main.colleges, state="readonly").place(x=150, y=130)

        tk.Label(self.labelframe, text="Start date and time:", bg="skyblue").place(x=70, y=180)
        self.start_date = DateEntry(self.labelframe, state="readonly")
        self.start_date.place(x=200, y=180)
        time_now = datetime.now()
        self.start_hour = tk.StringVar(value=time_now.hour)
        tk.Spinbox(self.labelframe, from_=0, to=23, wrap=True, width=3, state="readonly", textvariable=self.start_hour).place(x=300, y=180)
        self.start_min = tk.StringVar(value=time_now.minute)
        tk.Spinbox(self.labelframe, from_=0, to=59, wrap=True, width=3, state="readonly", textvariable=self.start_min).place(x=335, y=180)

        tk.Label(self.labelframe, text="End date and time:", bg="skyblue").place(x=70, y=220)
        self.end_date = DateEntry(self.labelframe, state="readonly")
        self.end_date.place(x=200, y=220)
        self.end_hour = tk.StringVar(value=time_now.hour)
        tk.Spinbox(self.labelframe, from_=0, to=23, wrap=True, width=3, state="readonly", textvariable=self.end_hour).place(x=300, y=220)
        self.end_min = tk.StringVar(value=time_now.minute)
        tk.Spinbox(self.labelframe, from_=0, to=59, wrap=True, width=3, state="readonly", textvariable=self.end_min).place(x=335, y=220)

        ttk.Button(self.labelframe, text="Reserve", command=self.reserve).place(x=220, y=290)

        self.labelframe2 = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        tk.Label(self.labelframe2, text="My Reservations", bg="skyblue", font=("Arial", 18, "bold")).place(x=150, y=60)

        self.tv_of_reserv = ttk.Treeview(self.labelframe2, height=7, columns=(1, 2, 3, 4), show="headings")
        self.tv_of_reserv.heading(1, text="Location")
        self.tv_of_reserv.column(1, minwidth=0, width=110, anchor=tk.CENTER)
        self.tv_of_reserv.heading(2, text="Plate Number")
        self.tv_of_reserv.column(2, minwidth=0, width=110, anchor=tk.CENTER)
        self.tv_of_reserv.heading(3, text="Start Date And Time")
        self.tv_of_reserv.column(3, minwidth=0, width=160, anchor=tk.CENTER)
        self.tv_of_reserv.heading(4, text="End Date And Time")
        self.tv_of_reserv.column(4, minwidth=0, width=160, anchor=tk.CENTER)
        self.tv_of_reserv.place(x=30, y=110)

        ttk.Button(self.labelframe2, text="Show", command=self.show).place(x=220, y=300)

        ttk.Button(self.frame, text="Logout", command=self.logout).place(x=405, y=360)

        self.notebook.add(self.labelframe, text="Reserve a Cart")
        self.notebook.add(self.labelframe2, text="View my Reservations")

    def reserve(self):
        sdate= self.start_date.get().split("/")
        startDate=datetime(2000+int(sdate[2]),int(sdate[0]),int(sdate[1]),int(self.start_hour.get()),int(self.start_min.get()))

        edate=self.end_date.get().split(("/"))
        endDate = datetime(2000 + int(edate[2]), int(edate[0]), int(edate[1]), int(self.end_hour.get()),int(self.end_min.get()))

        reserveTime = endDate-startDate
        maxFaculty= datetime(1, 1, 1,1,30) - datetime(1, 1, 1,0,0)
        maxEmployees= datetime(1, 1, 1,1,0) - datetime(1, 1, 1,0,0)
        maxStudents= datetime(1, 1, 1,0,30) - datetime(1, 1, 1,0,0)

        if reserveTime>maxFaculty: # reserve time > 01:30
            return messagebox.showerror(title="Time exceed",message="you can't resereve a cart for that long time")
        elif reserveTime > maxEmployees and self.userClass == "employee": # resereve time > 01:00 for an employee
            return messagebox.showerror(title="Time exceed",message="you can't resereve a cart for that long time")
        elif reserveTime > maxStudents and self.userClass == "Student": #reserveTime > 00:30 for a student
            return messagebox.showerror(title="Time exceed",message="you can't resereve a cart for that long time")
        else:
            conn = sqlite3.connect("ksu_golf_carts.db")
            sql = ("SELECT plate_number FROM golf_carts WHERE college = ?")
            col = (self.college.get(),)
            carts = list(conn.execute(sql, col))

            for plate in carts:
                sql = ("SELECT start_time as '[timestamp]', end_time as '[timestamp]' FROM reservations WHERE plate_number = ?")
                col = plate
                reservedDates = list(conn.execute(sql, col))
                noConflict=True
                for date in reservedDates:
                    date=list(date)
                    startReserved = datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S')
                    endReserved = datetime.strptime(date[1], '%Y-%m-%d %H:%M:%S')

                    if startReserved <= startDate <= endReserved:
                        noConflict=False
                    elif startReserved <= endDate <= endReserved:
                        noConflict=False
                    elif startDate <= startReserved and endDate >= endReserved:
                        noConflict=False

                if noConflict==True:
                    sql = "INSERT INTO reservations (plate_number, user_id, start_time, end_time) VALUES (?,?,?,?)"
                    values = (plate[0], self.userID, startDate, endDate)
                    print(values)
                    conn.execute(sql, values)
                    conn.commit()
                    return messagebox.showinfo(title="Reserved", message="You reserved cart with plate number '{}' from '{}' college at '{}' to '{}'".format(plate[0], self.college.get(), startDate, endDate))
            return messagebox.showerror(title="No carts", message="There is no carts available from this college at this time.")

    def show(self):
        self.tv_of_reserv.delete(*self.tv_of_reserv.get_children())
        conn = sqlite3.connect("ksu_golf_carts.db")
        sql = ("SELECT golf_carts.college, reservations.plate_number, reservations.start_time, reservations.end_time FROM reservations JOIN golf_carts ON golf_carts.plate_number=reservations.plate_number WHERE user_id = ?")
        col = (self.userID,)
        reservations = list(conn.execute(sql, col))
        for res in reservations:
            self.tv_of_reserv.insert(parent="", index=0, values=(res[0], res[1], res[2],res[3]))
        # for i, data in enumerate([(x, x+5, x+10) for x in range(5)]):
        #     self.tv_of_reserv.insert(parent="", index=i, values=data)

    def logout(self):
        self.main.change_page("signup")