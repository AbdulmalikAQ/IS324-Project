import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class User:
    def __init__(self, main, args = {}):
        self.main = main
        self.frame = tk.Frame(self.main.window, width=500, height=400, bg="skyblue")
        self.frame.grid_propagate(0)
        self.frame.grid()

        style = ttk.Style()
        style.configure("TNotebook", background="skyblue")
        style.theme_use("clam")
        style.configure("Treeview", background="#F0F0F0", fieldbackground="#F0F0F0")

        self.notebook = ttk.Notebook(self.frame)
        self.notebook.place(x=0, y=0)

        tk.Label(self.frame, text="Weclome, {} {}!".format(args.get("first_name"), args.get("last_name")), bg="skyblue").place(x=20, y=45)

        self.labelframe = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        tk.Label(self.labelframe, text="Reserve a Cart", bg="skyblue", font=("Arial", 18, "bold")).place(x=160, y=60)

        tk.Label(self.labelframe, text="College:", bg="skyblue").place(x=70, y=130)
        self.college = tk.StringVar(value=self.main.colleges[0])
        self.cb = ttk.Combobox(self.labelframe, width=40, textvariable=self.college, values=self.main.colleges, state="readonly").place(x=150, y=130)

        tk.Label(self.labelframe, text="Start date and time:", bg="skyblue").place(x=70, y=180)
        start_date = DateEntry(self.labelframe, state="readonly")
        start_date.place(x=200, y=180)
        time_now = datetime.now()
        start_hour = tk.StringVar(value=time_now.hour)
        tk.Spinbox(self.labelframe, from_=0, to=23, wrap=True, width=3, state="readonly", textvariable=start_hour).place(x=300, y=180)
        start_min = tk.StringVar(value=time_now.minute)
        tk.Spinbox(self.labelframe, from_=0, to=59, wrap=True, width=3, state="readonly", textvariable=start_min).place(x=335, y=180)

        tk.Label(self.labelframe, text="End date and time:", bg="skyblue").place(x=70, y=220)
        end_date = DateEntry(self.labelframe, state="readonly")
        end_date.place(x=200, y=220)
        end_hour = tk.StringVar(value=time_now.hour)
        tk.Spinbox(self.labelframe, from_=0, to=23, wrap=True, width=3, state="readonly", textvariable=end_hour,).place(x=300, y=220)
        end_min = tk.StringVar(value=time_now.minute)
        tk.Spinbox(self.labelframe, from_=0, to=59, wrap=True, width=3, state="readonly", textvariable=end_min).place(x=335, y=220)

        tk.Button(self.labelframe, text="Reserve", width=10, command=self.reserve).place(x=220, y=290)

        self.labelframe2 = tk.Frame(self.notebook, bg="skyblue", width=500, height=400)

        tk.Label(self.labelframe2, text="My Reservations", bg="skyblue", font=("Arial", 18, "bold")).place(x=150, y=60)

        self.tv_of_reserv = ttk.Treeview(self.labelframe2, height=7, columns=(1, 2, 3), show="headings")
        self.tv_of_reserv.heading(1, text="Plate Number")
        self.tv_of_reserv.column(1, minwidth=0, width=110, anchor=tk.CENTER)
        self.tv_of_reserv.heading(2, text="Start Date And Time")
        self.tv_of_reserv.column(2, minwidth=0, width=160, anchor=tk.CENTER)
        self.tv_of_reserv.heading(3, text="End Date And Time")
        self.tv_of_reserv.column(3, minwidth=0, width=160, anchor=tk.CENTER)
        self.tv_of_reserv.place(x=30, y=110)

        tk.Button(self.labelframe2, text="Show", width=10, command=self.show).place(x=220, y=300)

        tk.Button(self.frame, text="Logout", width=10, command=self.logout).place(x=405, y=360)

        self.notebook.add(self.labelframe, text="Reserve a Cart")
        self.notebook.add(self.labelframe2, text="View my Reservations")

    def reserve(self):
        messagebox.showwarning(title="Not Available Yet", message="Wait for the next version.")

    def show(self):
        self.tv_of_reserv.delete(*self.tv_of_reserv.get_children())
        self.tv_of_reserv.insert(parent="", index=0, values=("EDJ1232", "2023-11-19 23:55", "2023-11-20 00:25"))
        # for i, data in enumerate([(x, x+5, x+10) for x in range(5)]):
        #     self.tv_of_reserv.insert(parent="", index=i, values=data)

    def logout(self):
        self.main.change_page("signup")