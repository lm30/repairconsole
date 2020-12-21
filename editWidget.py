from tkinter import *
import tkinter as tk
import datetime
import mysql.connector as mysql

class EditWidget(object):
	def __init__(self, root=None, **kwargs):
		self.root = root
		self.dbinfo = kwargs.pop('dbinfo')
		self.model = kwargs.pop("model")
		self.table = kwargs.pop("table")

	def createWidget(self, recordKey, recordToMod):
		pass

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
			elif key == "repairnumber" and recordToMod[key]:
				field = tk.StringVar(window)
				field.set(recordToMod[key])
				entry = Entry(window, textvariable=field, state='disabled')
			else:
				field = tk.StringVar(window)
				field.set(recordToMod[key])
				entry = tk.Entry(window, textvariable=field)
			modifyFields[key] = field
			if entry: entry.grid(row=i, column=j + 1, sticky="nsew")
			i += 1
			maxRow = max(maxRow, i)

		return modifyFields, maxRow

	def updateDatabase(self, query, values=None):
		# update and commit to the databse
		# will autocommit to the database
		# db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'], autocommit=True)
		
		# for testing purposes, keep this uncommented
		db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])

		cursor = db_connection.cursor()
		if values:
			cursor.execute(query, values)
		else:
			cursor.execute(query)
		cursor.close()
		db_connection.close()

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


	def addComment(self, recordKey, comment):
		newComment = comment
		if not recordKey: 
			oldComment = None
		else:
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