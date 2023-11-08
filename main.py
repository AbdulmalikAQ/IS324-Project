import tkinter as tk
import sqlite3

from pages.login import Login
from pages.signup import SignUp

pages = {
	"login": Login,
	"signup": SignUp
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
conn.commit()
conn.close()

class Main:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("KSU Golf Carts")

		self.current_page = Login(self)

		self.window.mainloop()

	def change_page(self, page_name):
		self.current_page.frame.destroy()
		self.current_page = pages.get(page_name)(self)

if __name__ == "__main__":
	Main()