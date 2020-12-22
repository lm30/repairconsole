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

		self.dbinfo = {}
		self.setup()

	def setup(self):
		# make the window full screen width and half the height
		width = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.geometry(f'{width}x{height}')

		# setting the frame as pack
		frame = tk.Frame(self.root)
		frame.pack()

		self.readDBFile()
		self.createRepairTable()

		addItemBtn = tk.Button(self.root, text="Add item", command=self.repTable.addItemWidget)
		addItemBtn.pack(fill=tk.BOTH,side=tk.RIGHT, expand=True)

		buttonOverdue = self.repTable.createOverdueButton(self.root)
		buttonOverdue.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)

	def readDBFile(self):
		with open("dbInfoFile.txt", "r") as datafile:
			for line in datafile:
				lineList = line.split(" ")
				self.dbinfo[lineList[0]] = lineList[-1]

	def createRepairTable(self):
		self.repTable = RepairTableGUI(self.root, dbinfo=self.dbinfo)
		self.repTable.createRepairWidget()

	def closeGUI(self):
		# upon clicking the red "X" to close the application
		# if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
		self.root.destroy()

def main():
	root = tk.Tk()
	repairGUI = RepairGUI(root, title="Repair Console")
	root.mainloop()

if __name__ == '__main__':
	main()