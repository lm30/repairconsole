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

	def addItemWidget(self):
		window = tk.Toplevel()
		window.title("Add entry")
		window.resizable(False, False)

		# redo this whole part. see todo list for details on how should do it
		fields = {
					"repairnumber": "", 
					"firstname":"",
					"lastname":"",
					"email":"",
					"phone":"",
					"daterecieved":"",
					"repairedby":"",
					"comments":"",
					"typeof":"",
					"manufacturer":"",
					"model":"",
					"status":"",
		}
		fields, rows = self.createWidgetFields(window, fields)

		tk.Button(window, text="save", command= lambda arg1=fields, arg2=window : self.addItem(fields, window)).grid(columnspan=4, sticky="nsew")

		window.bind("<Escape>", lambda e: window.destroy())
		window.protocol("WM_DELETE_WINDOW", window.destroy)

	def addItem(self, fields, window):
		# redo this whole function.
		addedItems = {}
		for item in fields:
			if isinstance(fields[item], scrolledtext.ScrolledText): 
				addedItems[item] = self.addComment(None, fields[item].get("1.0", "end-1c"))
			else:
				if item == "repairnumber" and not fields[item].get():
					messagebox.showerror("Unable to add item", "Repair number cannot be left blank")
					return
				elif item == "repairnumber" and fields[item].get().isdigit() == False:
					messagebox.showerror("Unable to add item", "Repair number must be a whole number")
					return
				elif item == "daterecieved":
					today = datetime.datetime.today().strftime('%Y-%m-%d')
					addedItems[item] = today
					if fields[item].get():
						date = fields[item].get()
						if not self.isValidDate(date):
							return
						addedItems[item] = date
					addedItems["lastupdated"] = today
				else:
					addedItems[item] = fields[item].get()

		# add row in the table
		key = self.model.addRow(**addedItems)
		self.repairTable.redraw()

		query, valuesList = self.createAddQuery(addedItems)
		# update and commit to the databse
		# will autocommit to the database
		db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'], autocommit=True)
		
		# for testing purposes, keep this uncommented
		# db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])
		
		cursor = db_connection.cursor()
		cursor.execute(query, valuesList)
		cursor.close()
		db_connection.close()

		window.destroy()

	def createModifyWidget(self, recordKey, recordToMod):
		window = tk.Toplevel()
		windowTitle = "Repair Number: " + str(recordToMod['repairnumber'])
		window.resizable(False, False)
		window.title(windowTitle)

		modifyFields, maxRow = self.createWidgetFields(window, recordToMod)

		# change the column and column span so don't have to manually change if more cols appear than 4
		# why are the buttons not changing colors?
		tk.Button(window, text="delete", bg='#8eeda8', command= lambda arg1=recordKey, arg2=window: self.deleteRow(arg1, arg2)).grid(row=maxRow + 1, column=0, columnspan=2, sticky=N+S+W+E)
		tk.Button(window, text="save", bg='black', command= lambda arg1=recordKey, arg2=modifyFields : self.saveModifications(arg1, arg2)).grid(row=maxRow + 1, column=2, columnspan=2, sticky=N+S+E+W)

		# makes sure destroys self when click the "X" to close
		window.bind('<Escape>', lambda e: window.destroy())
		window.protocol("WM_DELETE_WINDOW", window.destroy)

	# finish editing this so can reuse for add widget
	def createWidgetFields(self, window, recordToMod):
		i = 1
		j = 0
		maxRow = i
		modifyFields = {}
		# simplify this later
		for key in recordToMod.keys():
			tk.Label(window, text=key, font="Arial 16 bold").grid(row=i, column=j, sticky=W)
			field = None
			entry = None
			if key == "comments":
				field = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
				field.grid(row=i, column=j + 1, sticky="nsew")
				if recordToMod[key]: field.insert(INSERT, recordToMod[key]) 
				j += 2
				i = 0
			elif key == "status":
				field = tk.StringVar(window)
				options = ["received", "inspected", "in progress", "finished", "shipped" ]
				if not recordToMod[key]: field.set(options[0])
				else: field.set(recordToMod[key])
				entry = tk.OptionMenu(window, field, *options)
			elif key == "typeof":
				field = tk.StringVar(window)
				options = ["amplifier", "amplified speaker", "cassette player", "cartridge", "cd player","compact system", "preamp", "receiver", "reel to reel", "turntable", "tuner", "voltage conversion", "other"]
				if not recordToMod[key]: field.set(options[0])
				else: field.set(recordToMod[key])
				entry = tk.OptionMenu(window, field, *options)
			# elif key == "repairnumber":
				# tk.Label(window, text=recordToMod[key], font="Arial 16 bold").grid(row=i, column=j + 1, sticky="nsew")
			else:
				field = tk.StringVar(window)
				field.set(recordToMod[key])
				entry = tk.Entry(window, textvariable=field)
			modifyFields[key] = field
			if entry: entry.grid(row=i, column=j + 1, sticky="nsew")
			i += 1
			maxRow = max(maxRow, i)

		return modifyFields, maxRow

	def deleteRow(self, rowNumber, window):
		# remove entry from the table, and db then close the window
		raNumber = self.model.getData()[rowNumber]["repairnumber"]
		del self.model.data[rowNumber]
		self.model.reclist.remove(rowNumber)
		self.repairTable.redraw()

		query = "delete from repairconsole where repairnumber=" + str(raNumber)
		# update and commit to the databse
		# will autocommit to the database
		# db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'], autocommit=True)
			
		# for testing purposes, keep this uncommented
		db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])

		cursor = db_connection.cursor()
		cursor.execute(query)
		cursor.close()
		db_connection.close()

		window.destroy()

	# { recordkey : record at that key regardless of whether is same }
	def saveModifications(self, recordKey, fields):
		updated = self.findUpdatedFields(recordKey, fields)
		if updated:
			# change self.data and the canvas and update the db
			for key in updated:
				# self.data[recordKey][key] = updated[key]
				self.insertText(fields[key], updated[key])

			# edit the table for the user
			# self.editRow(recordKey, self.data[recordKey])
			self.editRow(recordKey, updated)
			self.repairTable.redraw()

			query = self.createUpdateQuery(updated, recordKey)
			# update and commit to the databse
			# will autocommit to the database
			# db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'], autocommit=True)
			
			# for testing purposes, keep this uncommented
			db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])

			cursor = db_connection.cursor()
			cursor.execute(query)
			cursor.close()
			db_connection.close()

	def insertText(self, textfield, text):
		if isinstance(textfield, tk.StringVar):
			textfield.set(text)
		else:
			textfield.delete("1.0", END)
			textfield.insert("1.0", text)

	def editRow(self, recordKey, updatedFields):
		for key in updatedFields:
			self.model.data[recordKey][key] = updatedFields[key]

	def createUpdateQuery(self, updatedRows, recordKey):
		query = "update repairconsole set "

		for key in updatedRows:
			query += "`" + key + "` = \'%s\'" % (updatedRows[key]) + ","
		# query = query[:len(query) - 1] + " where repairnumber = " + str(self.data[recordKey]['repairnumber'])
		query = query[:len(query) - 1] + " where repairnumber = " + str(self.model.getData()[recordKey]['repairnumber'])
		return query

	def createAddQuery(self, addedColumns):
		# since addedColumns is a dictionary, and order isn't necessarily preserved here
		# need to return the tuple for the values too
		query = "insert into repairconsole "
		fields = "("
		values = "VALUES (" + (", %s" * len(addedColumns))[2:] + ")"

		valuesList = []
		for item in addedColumns:
			fields += item + ", "
			valuesList.append(addedColumns[item])
		query += fields[:-2] + ") " + values

		return query, tuple(valuesList)

	def findUpdatedFields(self, recordKey, fields):
		## DO NOT ALLOW CHANGES TO THE RA NUMBER. THIS IS A PART THAT WILL NEVER CHANGE FOR A ROW
		updatedDict = {}
		for key in fields:
			# change to check if is instance of scrolled text THEN if is comments key
			if key == 'comments':
				comments = fields[key].get("1.0", "end-1c")
				# if comments and comments != self.data[recordKey][key]:
				if comments and comments != self.model.getData()[recordKey][key]:
					# change the comment in the field itself when saving
					comment = self.addComment(recordKey, comments)
					updatedDict[key] = comment
			elif key == "daterecieved" or key == "lastupdated":
				# if fields[key].get() != self.data[recordKey][key] and self.isValidDate(fields[key].get()):
				if fields[key].get() != self.model.getData()[recordKey][key] and self.isValidDate(fields[key].get()):
					updatedDict[key] = fields[key].get()
			# elif key == "repairnumber" and (int(fields[key].get()) != self.data[recordKey][key]):
			elif key == "repairnumber" and (int(fields[key].get()) != self.model.getData()[recordKey][key]):
				updatedDict[key] = int(fields[key].get())
			# elif key != "repairnumber" and fields[key].get() != self.data[recordKey][key]:
			elif key != "repairnumber" and fields[key].get() != self.model.getData()[recordKey][key]:
				updatedDict[key] = fields[key].get()

		return updatedDict

	def addComment(self, recordKey, comment):
		newComment = comment
		if not recordKey: 
			oldComment = None
		else:
			# oldComment = self.data[recordKey]["comments"]
			oldComment = self.model.getData()[recordKey]["comments"]

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
		else:
			return ""

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
			# print("entire record: ", self.repairTable.model.getRecordAtRow(clicks[0]))
			recKey = self.repairTable.model.getRecName(clicks[0])
			self.createModifyWidget(recKey ,self.repairTable.model.getRecordAtRow(clicks[0]))
				# print(clicks[0])
				# self.repairTable.setSelectedRow(clicks[0])
			# except: print("no records at, ", clicks)

	def onMouseWheel(self, event):
		# mouse wheel for teh repair table scrolling
		# print(event.delta)
		self.repairTable.yview("scroll", event.delta, "units")