import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

import datetime
from tkintertable import TableCanvas, TableModel
import mysql.connector as mysql

from repairTableGUI import RepairTableGUI

class RepairGUI(object):
	def __init__(self, root=None, **kwargs):
		
		self.title = kwargs.pop('title')
		self.root = root
		self.root.title(self.title)
		self.root.protocol("WM_DELETE_WINDOW", self.closeGUI)

		# make the window full screen width and half the height
		width = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.geometry(f'{width}x{height}')

		# setting the frame as pack
		frame = tk.Frame(self.root, **kwargs)
		frame.pack()

		# create the widgets
		self.create_widgets()

		# add item button is place at the bottom -- change this later
		button_bonus = tk.Button(self.root, text="Add item", command=self.createAddWidget)
		button_bonus.pack(fill='x')

	def create_widgets(self):
		self.createRepairTable()

	def createRepairTable(self):
		dbinfo = {
		'host' : "108.167.140.132",
		'database' : 'zephyr44_repair',
		'user' : 'zephyr44_testus',
		'password' : 'password'
		}

		self.repTable = RepairTableGUI(self.root, dbinfo=dbinfo)
		self.repTable.createRepairWidget()

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