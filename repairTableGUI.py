from tkinter import *
import tkinter as tk
from tkintertable import TableCanvas, TableModel
import datetime
import mysql.connector as mysql

class RepairTableGUI(object):
	def __init__(self, root=None, **kwargs):
		self.root = root
		self.dbinfo = kwargs.pop('dbinfo')

	def createRepairWidget(self):
		self.createSearchWidget()
		self.createTableWidget()

	def createTableWidget(self):
		self.repairFrame = Frame(self.root)
		# change to grid?
		self.repairFrame.pack(side=TOP, fill='both', expand=True)

		self.getRepairs()
		self.model = TableModel()
		self.model.importDict(self.data)
		self.repairTable = TableCanvas(self.repairFrame, model=self.model, cellwidth=30, cellbackgr='#e3f698', thefont=('Arial', 12), rowheight=50, rowheaderwidth=50, rowselectedcolor='yellow', editable=False, read_only=True)
		self.repairTable.grid(row=50, stick=S)

		self.repairTable.createTableFrame()
		self.repairTable.show()

		self.repairTable.bind('<ButtonRelease-1>', self.clicked)
		self.repairTable.bind('<MouseWheel>', self.onMouseWheel)

	def createSearchWidget(self):
		self.searchFrame = Frame(self.root)
		self.searchFrame.pack(side=TOP, fill="x", expand=True)

		self.searchStr = tk.StringVar(self.searchFrame)
		self.searchStr.set('Search by RA')

		self.searchmenu = tk.OptionMenu(self.searchFrame, self.searchStr, 'Search by RA', "Search by Last name", "Search by model", "Search by Manufacturer", "Search by status")
		self.searchenter = tk.Entry(self.searchFrame)
		self.searchbutton = tk.Button(self.searchFrame, text="Search") # command = self.searching
		self.refresh = tk.Button(self.searchFrame, text="Refresh") # command = self.getRepairs

		i = 0
		self.searchenter.grid(row=0, column= i)
		self.searchmenu.grid(row=0, column= i + 1)
		self.searchbutton.grid(row=0, column= i + 2)
		self.refresh.grid(row=0, column= i + 3)

	def getRepairs(self):
		db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])

		cursor = db_connection.cursor(dictionary=True)
		cursor.execute("select * from repairconsole")
		entries = cursor.fetchall()

		self.data = {}
		for i in range(len(entries)):
			self.data[i] = entries[i]
			if isinstance(entries[i]['daterecieved'], datetime.date):
				self.data[i]['daterecieved'] = str(entries[i]['daterecieved'])
			if isinstance(entries[i]['last updated'], datetime.date):
				self.data[i]['last updated'] = str(entries[i]['last updated'])

		cursor.close()
		db_connection.close()


	def createModifyWidget(self, recordKey, recordToMod):
		window = tk.Toplevel()
		windowTitle = "Repair Number: " + str(recordToMod['repairnumber'])
		window.title(windowTitle)

		i = 1
		j = 0
		for key in recordToMod.keys():
			tk.Label(window, text=key, font="Arial 16 bold").grid(row=i, column=j, sticky=W)
			if key == "comments":
				textfield = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
				textfield.grid(row=i, column=j + 1)
				if recordToMod[key]: textfield.insert(INSERT, recordToMod[key]) 
				j += 2
				i = 1
			else:
				entry = tk.Entry(window)
				if recordToMod[key]:
					entry.insert(0, recordToMod[key])
				entry.grid(row=i, column=j + 1)
				i += 1

		# change the column and column span so don't have to manually change if more cols appear than 4
		tk.Button(window, text="save", bg='black', command=self.save_modifications).grid(columnspan=4, sticky=S+E+W)

		# makes sure destroys self when click the "X" to close
		window.bind('<Escape>', lambda e: window.destroy())
		window.protocol("WM_DELETE_WINDOW", window.destroy)

	# { recordkey : record at that key regardless of whether is same }
	def save_modifications(self):
		pass


	def clicked(self, event):
		try:
			rclicked = self.repairTable.get_row_clicked(event)
			cclicked = self.repairTable.get_col_clicked(event)
			clicks = (rclicked, cclicked)
		except:
			print("error")
		if clicks:
			# try: 
			print("entire record: ", self.repairTable.model.getRecordAtRow(clicks[0]))
			recKey = self.repairTable.model.getRecName(clicks[0])
			self.createModifyWidget(recKey ,self.repairTable.model.getRecordAtRow(clicks[0]))
				# print(clicks[0])
				# self.repairTable.setSelectedRow(clicks[0])
			# except: print("no records at, ", clicks)

	def onMouseWheel(self, event):
		# mouse wheel for teh repair table scrolling
		print(event.delta)
		self.repairTable.yview("scroll", event.delta, "units")