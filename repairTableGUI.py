from tkinter import *
import tkinter as tk
from tkintertable import TableCanvas, TableModel
import datetime
import mysql.connector as mysql

from overdueTable import OverdueTable
from modifyWindow import ModifyWindow
from addItemWindow import AddItemWindow
from columnName import ColumnName


class RepairTableGUI(object):
	def __init__(self, root=None, **kwargs):
		self.root = root
		self.dbinfo = kwargs.pop('dbinfo')

	def createRepairWidget(self):
		self.createSearchWidget()
		self.createTableWidget()

		self.modifyWidget = ModifyWindow(dbinfo=self.dbinfo, model=self.model, table=self.repairTable)
		self.addWidget = AddItemWindow(dbinfo=self.dbinfo, model=self.model, table=self.repairTable)

	def createOverdueButton(self, parent):
		overdueTracker = OverdueTable(self.root, dbinfo=self.dbinfo)
		button = tk.Button(parent, text="Overdue", command=overdueTracker.createOverdueTable, bg="black", fg="red")
		button.bind("<Destroy>", lambda x: overdueTracker.stopSchedule())
		return button

	def createTableWidget(self):
		self.repairFrame = Frame(self.root)
		self.repairFrame.pack(side=TOP, fill='both', expand=True)

		self.model = TableModel()
		self.repairTable = TableCanvas(self.repairFrame, model=self.model, cellwidth=30, cellbackgr='#e3f698', thefont=('Arial', 12), rowheight=50, rowheaderwidth=50, rowselectedcolor='yellow', editable=False, read_only=True)		
		self.repairTable.grid(row=50, stick=S)
		
		self.getRepairs()

		self.repairTable.createTableFrame()
		self.sortTable()
		self.repairTable.show()

		self.repairTable.bind('<ButtonRelease-1>', self.clicked)
		self.repairTable.bind('<MouseWheel>', self.onMouseWheel)

	def createSearchWidget(self):
		self.searchFrame = Frame(self.root)
		self.searchFrame.pack(side=TOP, fill="x", expand=False)

		self.searchStr = tk.StringVar(self.searchFrame)
		self.searchStr.set('Search by RA')

		self.searchmenu = tk.OptionMenu(self.searchFrame, self.searchStr, 'Search by RA', "Search by last name", "Search by model", "Search by manufacturer", "Search by status")
		self.searchenter = tk.Entry(self.searchFrame)
		self.searchbutton = tk.Button(self.searchFrame, text="Search", command=self.searchRepairs) # command = self.searching
		self.refresh = tk.Button(self.searchFrame, text="Refresh", command=self.refreshRepairs) # command = self.getRepairs

		self.sortStr = tk.StringVar(self.searchFrame)
		self.sortStr.set('Sort by RA')
		self.sortmenu = tk.OptionMenu(self.searchFrame, self.sortStr, "Sort by RA", "Sort by last name", "Sort by date recieved", "Sort by last updated", "Sort by status", "Sort by type")

		i = 0
		self.refresh.grid(row=0, column= i)
		self.searchenter.grid(row=0, column= i + 1)
		self.searchmenu.grid(row=0, column= i + 2)
		self.sortmenu.grid(row=0, column=i + 3, columnspan=2)
		self.searchbutton.grid(row=0, column= i + 6)

	def searchRepairs(self):
		# redo this function
		# also what to do to get back to showing all? Refresh button or blank search space?
		query = self.createSearchQuery()
		entries = self.queryDatabase(query, useDict=True)

		data = {}
		for i in range(len(entries)):
			data[i] = self.changeRowToReadable(entries[i])
			# data[i] = entries[i]
			# if isinstance(entries[i]['daterecieved'], datetime.date):
			# 	data[i]['daterecieved'] = str(entries[i]['daterecieved'])
			# if isinstance(entries[i]['lastupdated'], datetime.date):
			# 	data[i]['lastupdated'] = str(entries[i]['lastupdated'])

		self.model.deleteRows()
		self.model.importDict(data)
		self.repairTable.redraw()
		self.sortTable()

	def refreshRepairs(self):
		self.model.deleteRows()
		self.getRepairs()
		self.repairTable.redraw()
		self.sortTable()

	def getRepairs(self):
		entries = self.queryDatabase("select * from repairconsole", useDict=True)
		data = {}
		for i in range(len(entries)):
			data[i] = self.changeRowToReadable(entries[i])
			# if isinstance(data[i][ColumnName["daterecieved"].value], datetime.date):
			# 	data[i][ColumnName["daterecieved"].value] = str(data[i][ColumnName["daterecieved"].value])
			# if isinstance(data[i][ColumnName["lastupdated"].value], datetime.date):
			# 	data[i][ColumnName["lastupdated"].value] = str(data[i][ColumnName["lastupdated"].value])
			

			# data[i] = entries[i]
			# if isinstance(entries[i]['daterecieved'], datetime.date):
			# 	data[i]['daterecieved'] = str(entries[i]['daterecieved'])
			# if isinstance(entries[i]['lastupdated'], datetime.date):
			# 	data[i]['lastupdated'] = str(entries[i]['lastupdated'])

		# print(data)

		self.model.importDict(data)

	def changeRowToReadable(self, entry):
		result = {}
		for key in entry:
			# to change column name to a readable version
			if key in ColumnName._member_names_: 
				newColName = ColumnName[key].value
				result[newColName] = entry[key]
			else:
				result[key] = entry[key]

		# to convert datetime to string
		if isinstance(result[ColumnName['daterecieved'].value], datetime.date):
			result[ColumnName["daterecieved"].value] = str(result[ColumnName["daterecieved"].value])
		if isinstance(result[ColumnName['lastupdated'].value], datetime.date):
			result[ColumnName["lastupdated"].value] = str(result[ColumnName["lastupdated"].value])

		return result

	def sortTable(self):
		sortOption = self.sortStr.get()
		column = ColumnName["repairnumber"].value
		if sortOption == "Sort by last name":
			column = ColumnName["lastname"].value
		elif sortOption == "Sort by date recieved":
			column = ColumnName["daterecieved"].value
		elif sortOption == "Sort by last updated":
			column = ColumnName["lastupdated"].value
		elif sortOption == "Sort by status":
			column = ColumnName["status"].value
		elif sortOption == "Sort by type":
			column = ColumnName["typeof"].value

		self.repairTable.sortTable(columnName=column)

	def addItemWidget(self):
		self.addWidget.createWidget()

	def createSearchQuery(self):
		if self.searchenter.get() == "":
			return "select * from repairconsole"

		query = "select * from repairconsole where "
		option = self.searchStr.get()
		searchString = ""
		if option == "Search by RA": 
			searchString = "repairnumber = " + self.searchenter.get()
		if option == "Search by last name": 
			searchString = "lastname = \'%s\'" % (self.searchenter.get())
		elif option == "Search by model": 
			searchString = "model = \'%s\'" % (self.searchenter.get())
		elif option == "Search by manufacturer": 
			searchString = "manufacturer = \'%s\'" % (self.searchenter.get())
		elif option == "Search by statusof": 
			searchString = "status = \'%s\'" % (self.searchenter.get())
		
		return query + searchString

	def queryDatabase(self, query, useDict=False):
		# needs to catch errors if no results found
		db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])
		entries = {}
		cursor = db_connection.cursor(dictionary=useDict)
		try:
			cursor.execute(query)
			entries = cursor.fetchall()
		except:
			messagebox.showerror("No results found", "No entries found by specified parameters")
		cursor.close()
		db_connection.close()

		return entries

	def clicked(self, event):
		try:
			rclicked = self.repairTable.get_row_clicked(event)
			cclicked = self.repairTable.get_col_clicked(event)
			clicks = (rclicked, cclicked)
		except:
			print("error")
		if clicks:
			try: 
			# print("entire record: ", self.repairTable.model.getRecordAtRow(clicks[0]))
				recKey = self.repairTable.model.getRecName(clicks[0])
				self.modifyWidget.createWidget(recKey, self.repairTable.model.getRecordAtRow(clicks[0]))
				# self.createModifyWidget(recKey ,self.repairTable.model.getRecordAtRow(clicks[0]))
				# print(clicks[0])
				# self.repairTable.setSelectedRow(clicks[0])
			except:
				pass 

	def onMouseWheel(self, event):
		# mouse wheel for teh repair table scrolling
		self.repairTable.yview("scroll", event.delta, "units")