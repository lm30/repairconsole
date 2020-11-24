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
		self.repairTable.sortTable(columnName="repairnumber")
		self.repairTable.grid(row=50, stick=S)

		self.repairTable.createTableFrame()
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

		i = 0
		self.searchenter.grid(row=0, column= i + 1)
		self.searchmenu.grid(row=0, column= i + 2)
		self.searchbutton.grid(row=0, column= i + 3)
		self.refresh.grid(row=0, column= i)

	def searchRepairs(self):
		# redo this function
		# also what to do to get back to showing all? Refresh button or blank search space?
		db_connection = mysql.connect(
			host=self.dbinfo['host'], 
			database=self.dbinfo['database'], 
			user=self.dbinfo['user'], 
			password=self.dbinfo['password'])

		query = "select * from repairconsole where "
		option = self.searchStr.get()
		searchString = ""
		if option == "Search by RA": searchString = "repairnumber = " + self.searchenter.get()
		if option == "Search by last name": searchString = "lastname = \'%s\'" % (self.searchenter.get())
		elif option == "Search by model": searchString = "model = \'%s\'" % (self.searchenter.get())
		elif option == "Search by manufacturer": searchString = "manufacturer = \'%s\'" % (self.searchenter.get())
		elif option == "Search by statusof": searchString = "status = \'%s\'" % (self.searchenter.get())
		
		cursor = db_connection.cursor(dictionary=True)
		cursor.execute(query + searchString)
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

		# need to  see if will redo the whole thing without deleting all rows
		# or keep adding info to the model with each search
		self.model.deleteRows()
		self.model.importDict(self.data)
		# print(self.model)
		self.repairTable.redraw()

	def refreshRepairs(self):
		self.getRepairs()
		self.model.deleteRows()
		self.model.importDict(self.data)
		self.repairTable.redraw()

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
		modifyFields = {}
		for key in recordToMod.keys():
			tk.Label(window, text=key, font="Arial 16 bold").grid(row=i, column=j, sticky=W)
			if key == "comments":
				textfield = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
				textfield.grid(row=i, column=j + 1)
				modifyFields[key] = textfield
				if recordToMod[key]: textfield.insert(INSERT, recordToMod[key]) 
				j += 2
				i = 0
			elif key == "status":
				statusStr = tk.StringVar(window)
				statusStr.set(recordToMod[key])
				statusMenu = tk.OptionMenu(window, statusStr, "received", "inspected", "in progress", "finished", "shipped" )
				statusMenu.grid(row=i, column=j +1, sticky="nsew")
				modifyFields[key] = statusStr
			elif key == "typeof":
				typeStr = tk.StringVar(window)
				typeStr.set(recordToMod[key])
				typeMenu = tk.OptionMenu(window, typeStr, "amplifier", "amplified speaker", "cassette player", "cartridge", "cd player","compact system", "preamp", "receiver", "reel to reel", "turntable", "tuner", "voltage conversion", "other")
				typeMenu.grid(row=i, column=j + 1, sticky="nsew")
				modifyFields[key] = typeStr
			else:
				stringVar = tk.StringVar(window)
				stringVar.set(recordToMod[key])
				entry = tk.Entry(window, textvariable=stringVar)
				# modifyFields[key] = entry
				# if recordToMod[key]:
				# 	entry.insert(0, recordToMod[key])
				entry.grid(row=i, column=j + 1)
				modifyFields[key] = stringVar
			i += 1

		# change the column and column span so don't have to manually change if more cols appear than 4
		tk.Button(window, text="save", bg='black', command= lambda arg1=recordKey, arg2=modifyFields : self.save_modifications(arg1, arg2)).grid(columnspan=4, sticky=S+E+W)


		# makes sure destroys self when click the "X" to close
		window.bind('<Escape>', lambda e: window.destroy())
		window.protocol("WM_DELETE_WINDOW", window.destroy)

	# { recordkey : record at that key regardless of whether is same }
	def save_modifications(self, recordKey, fields):

		# update the db:
		updated = self.findUpdatedFields(recordKey, fields)
		if updated: # if it isn't empty
		# change self.data and the canvas and update the db
			for key in updated:
				self.data[recordKey][key] = updated[key]

			# REDO I don't like this because it means that the updated row changes, 
			# it shows up at the bottom of the table
			# will need to get the row and column and change that later
			self.model.deleteRow(key=recordKey)
			self.model.addRow(key=recordKey, **self.data[recordKey])
			self.repairTable.redraw()

			query = "update repairconsole set "

			db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])
			cursor = db_connection.cursor()
			cursor.execute(query)
			cursor.close()
			db_connection.close()

	def findUpdatedFields(self, recordKey, fields):
		updatedDict = {}
		for key in fields:
			if key == 'comments':
				if fields[key].get("1.0", "end-1c") != self.data[recordKey][key]:
					newComment = fields[key].get("1.0", "end-1c")
					oldComment = self.data[recordKey][key]
					if len(newComment) > len(oldComment):
						today = datetime.datetime.today().strftime('%Y-%m-%d')
						if newComment[len(oldComment)] == "\n":
							newComment = today + " " +  newComment[len(oldComment) + 1: ]
						else:
							newComment = today + " " + newComment[len(oldComment):]
					updatedDict[key] = oldComment + "\n" + newComment
			elif key == "daterecieved" or key == "last updated":
				if fields[key].get() != self.data[recordKey][key]:
					date = self.validateDate(fields[key].get())
					if date: updatedDict[key] = date
			elif key == "repairnumber" and (int(fields[key].get()) != self.data[recordKey][key]):
				updatedDict[key] = int(fields[key].get())
			elif key != "repairnumber" and fields[key].get() != self.data[recordKey][key]:
				updatedDict[key] = fields[key].get()

		return updatedDict

	# need a better name
	def validateDate(self, date_text):
		try:
			return datetime.datetime.strptime(date_text, '%Y-%m-%d')
		except ValueError:
			messagebox.showerror("Incorrect date format", "Incorrect date format, should be YYYY-MM-DD")
			return ""

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
		# print(event.delta)
		self.repairTable.yview("scroll", event.delta, "units")