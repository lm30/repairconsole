import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

import datetime
from tkintertable import TableCanvas, TableModel
import mysql.connector as mysql

from repairTableGUI import RepairTableGUI
from settingsWidget import SettingsWidget

class RepairGUI(object):
	def __init__(self, root=None, **kwargs):
		
		self.title = kwargs.pop('title')
		self.root = root
		self.root.title(self.title)
		self.root.protocol("WM_DELETE_WINDOW", self.closeGUI)

		self.frames = {}

		self.dbinfo = {}
		self.setup()

	def setup(self):
		# make the window full screen width and half the height
		width = self.root.winfo_screenwidth()
		height = self.root.winfo_screenheight()
		self.root.geometry(f'{width}x{height}')

		# self.container = tk.Frame(tk.Tk)
		# # container = tk.Frame(self.root)
		# self.container.pack(side=TOP, fill="both", expand=True)
		# self.container.grid_rowconfigure(0, weight=1)
		# self.container.grid_columnconfigure(0, weight=1)

		self.settingsWidget = SettingsWidget(self.root, settingFile="settings.txt")
		self.readDBFile()
		self.createRepairTable()

		self.settingsWidget.setOverdue()
		self.settingsWidget.setRepairTable(self.repTable)

		# self.frames["repairFrame"] = self.repTable.getFrame()
		# self.frames['settingsFrame'] = self.settingsWidget.getFrame()

		addItemBtn = tk.Button(
			self.root, 
			text="Add item", 
			command=self.repTable.addItemWidget
		)
		addItemBtn.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

		# buttonSettings = tk.Button(self.root, text="Settings", command=self.showFrame('settingsFrame'))
		# buttonSettings = tk.Button(self.root, text="Settings", command=self.settingsWidget)
		# buttonSettings.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

		buttonOverdue = self.repTable.createOverdueButton(self.root)
		buttonOverdue.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

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

	# def showFrame(self, frameName):
	# 	frame = self.frames[frameName]
	# 	frame.tkraise()

def main():
	root = tk.Tk()
	repairGUI = RepairGUI(root, title="Repair Console")
	root.mainloop()

if __name__ == '__main__':
	main()