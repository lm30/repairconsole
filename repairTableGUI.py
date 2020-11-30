from tkinter import *
import tkinter as tk
from tkintertable import TableCanvas, TableModel
import datetime
import mysql.connector as mysql

class RepairTableGUI(object):
	def __init__(self, root=None, **kwargs):
		self.root = root
		self.dbinfo = kwargs.pop('dbinfo')

		# # put this into an easily editable file later
		# self.columnInfo = {
		# 	"repairnumber": "Repair number",
		# 	"firstname": "First name",
		# 	"lastname": "Last name",
		# 	"email": "Email",
		# 	"phone": "Phone number",
		# 	"daterecieved": "Date recieved",
		# 	"lastupdated": "Last updated",
		# 	"repairedby": "Repaired by",
		# 	"comments": "Comments",
		# 	"typeof": "Type of",
		# 	"manufacturer": "Manufacturer",
		# 	"model": "Model",
		# 	"status": "Status"
		# }

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
		# self.repairTable.sortTable(columnName="repairnumber")
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
			if isinstance(entries[i]['lastupdated'], datetime.date):
				self.data[i]['lastupdated'] = str(entries[i]['lastupdated'])
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
			if isinstance(entries[i]['lastupdated'], datetime.date):
				self.data[i]['lastupdated'] = str(entries[i]['lastupdated'])

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
		if updated:
			# change self.data and the canvas and update the db
			for key in updated:
				self.data[recordKey][key] = updated[key]

			# edit the table for the user
			self.editRow(recordKey, self.data[recordKey])
			self.repairTable.redraw()

			query = self.createUpdateQuery(updated, recordKey)
			print(query)

			# update and commit to the databse
			# will autocommit to the database
			# db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'], autocommit=True)
			
			# for testing purposes, keep this uncommented
			db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])

			cursor = db_connection.cursor()
			cursor.execute(query)
			cursor.close()
			db_connection.close()

	def editRow(self, recordKey, updatedFields):
		for key in updatedFields:
			col = self.model.getColumnIndex(key)
			self.model.setValueAt(updatedFields[key], recordKey, col)

	def createUpdateQuery(self, updatedRows, recordKey):
		query = "update repairconsole set "

		for key in updatedRows:
			query += "`" + key + "` = \'%s\'" % (updatedRows[key]) + ","
		query = query[:len(query) - 1] + " where repairnumber = " + str(self.data[recordKey]['repairnumber'])
		return query

	def findUpdatedFields(self, recordKey, fields):
		## DO NOT ALLOW CHANGES TO THE RA NUMBER. THIS IS A PART THAT WILL NEVER CHANGE FOR A ROW
		updatedDict = {}
		for key in fields:
			if key == 'comments':
				comments = fields[key].get("1.0", "end-1c")
				if comments and comments != self.data[recordKey][key]:
					# change the comment in the field itself when saving
					comment = self.addComment(recordKey, comments)
					updatedDict[key] = comment
			elif key == "daterecieved" or key == "lastupdated":
				if fields[key].get() != self.data[recordKey][key] and self.isValidDate(fields[key].get()):
					updatedDict[key] = fields[key].get()
			elif key == "repairnumber" and (int(fields[key].get()) != self.data[recordKey][key]):
				updatedDict[key] = int(fields[key].get())
			elif key != "repairnumber" and fields[key].get() != self.data[recordKey][key]:
				updatedDict[key] = fields[key].get()

		return updatedDict

	def addComment(self, recordKey, comment):
		newComment = comment
		oldComment = self.data[recordKey]["comments"]

		# TODO: fix so user can modify previous comments AND add a new comment for that day
		# without using separate saves
		today = datetime.datetime.today().strftime('%Y-%m-%d')
		if not oldComment and newComment: # previously empty space and add new comment
			return today + ": " + newComment + "\n"
		elif (newComment and oldComment) and len(newComment) > len(oldComment):
			if newComment[:len(oldComment)] != oldComment:
				# if the user modified the comment for previous days
				return newComment + "\n"
			if newComment != oldComment:
				addedSegment = newComment[len(oldComment):]
				return oldComment + today + ": " + addedSegment + "\n"

	# need a better name
	def isValidDate(self, date_text):
		try:
			datetime.datetime.strptime(date_text, '%Y-%m-%d')
			if len(date_text) != 10:
				messagebox.showerror("Incorrect date format", "Incorrect date format, should be YYYY-MM-DD")
				return False
			return True
		except ValueError:
			messagebox.showerror("Incorrect date format", "Incorrect date format, should be YYYY-MM-DD")
			return False

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