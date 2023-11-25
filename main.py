import tkinter as tk
from tkinter import ttk
import sqlite3

from pages.login import Login
from pages.signup import SignUp
from pages.admin import Admin
from pages.user import User

pages = {
	"login": Login,
	"signup": SignUp,
	"admin": Admin,
	"user": User
}

constants = {
    "colleges": (
        "Computer Science and Information Technology",
    	"Business Administration",
    	"Engineering",
    	"Architecture and Planning",
    	"Food and Agriculture Sciences",
    	"Science"
	),
	"user_max_time": {
		"Factuly": 5400,
		"Employee": 3600,
		"Student": 1800
	}
}

conn = sqlite3.connect("ksu_golf_carts.db")
conn.execute('''
	CREATE TABLE IF NOT EXISTS users (
		user_id INT PRIMARY KEY NOT NULL,
		first_name TEXT NOT NULL,
		last_name TEXT NOT NULL,
		phone_number TEXT NOT NULL,
		user_class TEXT NOT NULL,
		email TEXT NOT NULL,
		password TEXT NOT NULL
	);
''')

conn.execute("INSERT OR IGNORE INTO users (user_id, first_name, last_name, email, phone_number, user_class, password) VALUES (?,?,?,?,?,?,?)", ("1234567890", "Admin", "1", "admin@ksu.edu.sa", "0555555555", "Admin", "3b612c75a7b5048a435fb6ec81e52ff92d6d795a8b5a9c17070f6a63c97a53b2"))
# Admin Account
# User ID: 1234567890
# Password: Admin123

conn.execute('''
	CREATE TABLE IF NOT EXISTS golf_carts (
		plate_number INT PRIMARY KEY NOT NULL,
		college TEXT NOT NULL
	);
''')

conn.execute('''
	CREATE TABLE IF NOT EXISTS reservations (
		plate_number INT NOT NULL,
		user_id INT NOT NULL,
		start_time TIMESTAMP NOT NULL,
		end_time TIMESTAMP NOT NULL,
		FOREIGN KEY (plate_number) REFERENCES golf_carts(plate_number),
		FOREIGN KEY (user_id) REFERENCES users(user_id)
	);
''')

conn.commit()
conn.close()

class Main:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("KSU Golf Carts")
		self.window.geometry("+600+200")

		ttk.Style().theme_use("clam")

		self.constants = constants
		self.current_page = pages.get("signup")(self)

		self.window.mainloop()

	def change_page(self, page_name, args = {}):
		self.current_page.frame.destroy()
		self.current_page = pages.get(page_name)(self, args)

if __name__ == "__main__":
	Main()