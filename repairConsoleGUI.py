import tkinter as tk
from tkinter import *
from tkinter import messagebox

from tkintertable import TableCanvas, TableModel
import mysql.connector as mysql

class RepairGUI(object):
	def __init__(self, root=None, **kwargs):
		
		self.title = kwargs.pop('title')
		self.root = root
		self.root.title(self.title)
		self.root.protocol("WM_DELETE_WINDOW", self.closeGUI)

		frame = tk.Frame(self.root, **kwargs)
		frame.pack()
		self.create_widgets()

		self.label = tk.Label(frame, text=self.title)
		self.label.pack(padx=10, pady=10)

		button_bonus = tk.Button(self.root, text="Add item", command=self.createAddWidget)
		button_bonus.pack(fill='x')

	def create_widgets(self):
		self.createRepairTable()

	def createRepairTable(self):
		HOST = "108.167.140.132"
		DATABASE = 'zephyr44_repair'
		USER = 'zephyr44_testus'
		PASSWORD = 'password'
		db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

		cursor = db_connection.cursor(dictionary=True)
		# add last date modified by too and daterecieved
		cursor.execute("select repairnumber, lastname, repairedby, status, typeof from repairconsole")
		entries = cursor.fetchall()
		print(entries)

		data = {i: entries[i] for i in range(len(entries))}
		print(data)
		# data = {0: {'repairnumber': 50000, 'lastname': 'doe', 'daterecieved': datetime.date(2020, 11, 16), 'repairedby': 'Pam', 'status': 'received', 'typeof': 'cassette player'}, 1: {'repairnumber': 50002, 'lastname': 'doe', 'daterecieved': datetime.date(2020, 10, 29), 'repairedby': 'Pam', 'status': 'inspected', 'typeof': 'amplifier'}}

		# colNames = cursor.column_names
		# print(colNames)

		# # repair frame is packed but it has grid style inside it
		# repairFrame = Frame(self.root)
		# repairFrame.pack(side=TOP, padx=0, pady=0)
		# for i in range(len(colNames)):
		# 	self.e = Entry(repairFrame, width=15, bg="red", fg='blue', font=('Arial', 16, 'bold'))
		# 	self.e.insert(END, colNames[i])
		# 	self.e.grid(row=0, column=i)
		# for i in range(len(entries)):
		# 	for j in range(len(entries[i])):
		# 		self.e = Entry(repairFrame, width=15, fg="black", font=('Arial', 12, 'bold'))
		# 		self.e.insert(END, entries[i][j])
		# 		self.e.grid(row=i + 1, column=j) # row + 1 to account for the column names


		# Tkintertable attempt
		repairFrame = Frame(self.root)
		repairFrame.pack(side=TOP)

		model = TableModel()
		model.importDict(data)
		table = TableCanvas(repairFrame, model=model, cellwidth=20, cellbackgr='#e3f698', thefont=('Arial', 12), rowheight=30, rowheaderwidth=50, rowselectedcolor='yellow', editable=False, read_only=True)
		table.createTableFrame()
		table.show()

	def closeGUI(self):
		# upon clicking the red "X" to close the application
		if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
			self.root.destroy()
		# self.master.destroy

	def createAddWidget(self):
		# change this to easily add entry to the database
		window = tk.Toplevel()
		window.title("Add entry")

		label = tk.Label(window, text="Under construction")
		label.pack(fill='x', padx=50, pady=5)

		# the escape button and clicking the close button will close the widget
		window.bind('<Escape>', lambda e: window.destroy())
		button_close = tk.Button(window, text="close", command=window.destroy)
		button_close.pack(fill='x')


def main():
	root = tk.Tk()
	repairGUI = RepairGUI(root, title="Repair Console")
	root.mainloop()

if __name__ == '__main__':
	main()