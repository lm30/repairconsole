from tkinter import *
import tkinter as tk
from tkintertable import TableCanvas, TableModel
import datetime
import mysql.connector as mysql

from threading import Timer


class OverdueTable(object):
	# an instance of this object should run once every day
	def __init__(self, root=None, **kwargs):
		self.root = root
		self.dbinfo = kwargs.pop('dbinfo')
		self.overdue = 50 # DAYS OVERDUE -- CHANGE LATER

		self.model = TableModel()
		self.updateOverdueEntries()
		self.setupTableSchedule()

	def setupTableSchedule(self):
		# 60 sec * 60 min * 24 hours 
		self.repeatingTimer = RepeatedTimer(30, self.updateOverdueEntries)

	def stopSchedule(self):
		self.repeatingTimer.stop()

	def createOverdueTable(self):
		window = tk.Toplevel()
		window.title("Overdue Table")

		# create table 
		overdueTable = TableCanvas(window, model=self.model, editable=False, read_only=True)		
		overdueTable.grid()
		overdueTable.createTableFrame()
		overdueTable.sortTable(columnName='daterecieved')
		overdueTable.show()

		window.bind("<Escape>", lambda e: window.destroy())
		window.protocol("WM_DELETE_WINDOW", window.destroy)

	def updateOverdueEntries(self):
		print("Checking for overdue entries in database...")
		entries = self.filterOverdueEntries()
		self.model.importDict(entries)

	def filterOverdueEntries(self):
		entries = self.getAllEntries(useDict=True)
		overdueEntries = {}
		i = 0
		for entry in entries:
			if self.checkOverdue(entry['daterecieved']):
				overdueEntries[i] = self.makeTableReadable(entry)
				i += 1
		return overdueEntries

	def getAllEntries(self, useDict=False):
		# query = "select * from repairconsole"
		query = "select repairnumber, lastname, daterecieved, lastupdated, status, repairedby, model, manufacturer, email, phone from repairconsole"
		# below doesn't work even when I use the sql statement directly 
		# query = "select * from repairconsole where daterecieved > %s"
		# query = "select * from repairconsole where daterecieved > " + str(self.getOverdueDate())
		db_connection = mysql.connect(host=self.dbinfo['host'], database=self.dbinfo['database'], user=self.dbinfo['user'], password=self.dbinfo['password'])
		entries = {}
		cursor = db_connection.cursor(dictionary=useDict)

		try:
			cursor.execute(query)
			entries = cursor.fetchall()
		except:
			messagebox.showerror("No overdue entries found", "No entries are overdue")
		cursor.close()
		db_connection.close()

		return entries

	def makeTableReadable(self, entry):
		if isinstance(entry['daterecieved'], datetime.date):
			entry['daterecieved'] = str(entry['daterecieved'])
		if isinstance(entry['lastupdated'], datetime.date):
			entry['lastupdated'] = str(entry['lastupdated'])
		return entry

	def checkOverdue(self, date):
		overdueDate = date + datetime.timedelta(days=self.overdue)
		if datetime.datetime.today().date() > overdueDate:
			return True
		return False

	# def getOverdueDate(self):
	# 	# returns datetime object 
	# 	date = datetime.datetime.today() - datetime.timedelta(days=self.overdue)
	# 	return date.replace(hour=0, minute=0, second=0, microsecond=0)

	# def isOverdue(self, datestring):
	# 	date = datetime.datetime.strptime(datestring,'%Y-%m-%d')
	# 	overdueDate =  date + datetime.timedelta(days=self.overdue)
	# 	if datetime.datetime.today() > overdueDate:
	# 		return True
	# 	return False

class RepeatedTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer = None
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.isRunning = False
		self.start()

	def start(self):
		if not self.isRunning:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.isRunning = True

	def _run(self):
		self.isRunning = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def stop(self):
		self._timer.cancel()
		self.isRunning = False