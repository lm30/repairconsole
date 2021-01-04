from tkinter import *
import tkinter as tk
import datetime
import mysql.connector as mysql

from editWidget import EditWidget
from columnName import ColumnName
from overdueTable import OverdueTable
from emailCreator.emailSMTPMaker import EmailSMTPMaker

class ModifyWindow(EditWidget):
	def __init__(self, root=None, **kwargs):
		super(ModifyWindow, self).__init__(root, **kwargs)
		self.emailHandler = EmailSMTPMaker(
			"emailCreator/emailTemplates/repairCompletedMessage.txt", 
			"emailCreator/emailInfo/testuser2020soundsmith.txt"
		)

	def createWidget(self, recordKey, recordToMod):
		window = tk.Toplevel()
		windowTitle = "Repair Number: " + str(recordToMod[ColumnName['repairnumber'].value])
		window.resizable(False, False)
		window.title(windowTitle)

		modifyFields, maxRow = self.createWidgetFields(window, recordToMod)

		# change the column and column span so don't have to manually change if more cols appear than 4
		# why are the buttons not changing colors?
		tk.Button(window, 
			text="delete", 
			bg='#8eeda8', 
			command= lambda arg1=recordKey, arg2=window : self.deleteRow(arg1, arg2)
		).grid(row=maxRow + 1, column=0, columnspan=2, sticky=N+S+W+E)
		
		tk.Button(window, 
			text="save", 
			bg='black', 
			command= lambda arg1=recordKey, arg2=modifyFields : self.saveModifications(arg1, arg2)
		).grid(row=maxRow + 1, column=2, columnspan=2, sticky=N+S+E+W)

		# makes sure destroys self when click the "X" to close
		window.bind('<Escape>', lambda e: window.destroy())
		window.protocol("WM_DELETE_WINDOW", window.destroy)

	def deleteRow(self, rowNumber, window):
		# remove entry from the table, and db then close the window
		# reset color
		self.colorRow(rowNumber, "#edfafa")
		raNumber = self.model.getData()[rowNumber][ColumnName["repairnumber"].value]
		self.model.deleteRow(rowNumber, rowNumber)
		# del self.model.data[rowNumber]
		# self.model.reclist.remove(rowNumber)
		self.table.redraw()
		self.table.sortTable(columnName=ColumnName['repairnumber'].value)

		query = "delete from repairconsole where repairnumber=" + str(raNumber)
		self.updateDatabase(query)

		window.destroy()

	# { recordkey : record at that key regardless of whether is same }
	def saveModifications(self, recordKey, fields):
		updated = self.findUpdatedFields(recordKey, fields)
		if updated:
			# change self.data and the canvas and update the db
			for key in updated:
				self.insertText(fields[key], updated[key])

			# edit the table for the user
			self.editRow(recordKey, updated)
			self.table.redraw()
			self.table.sortTable(columnName=ColumnName['repairnumber'].value)

			query = self.createUpdateQuery(updated, recordKey)
			self.updateDatabase(query)

	def insertText(self, textfield, text):
		if isinstance(textfield, tk.StringVar):
			textfield.set(text)
		else:
			textfield.delete("1.0", END)
			textfield.insert("1.0", text)

	def editRow(self, recordKey, updatedFields):
		for key in updatedFields:
			self.model.data[recordKey][key] = updatedFields[key]

		# this is essentially a copy from repairtableGUI, change this
		self.colorRow(recordKey, "#edfafa")
		if self.model.data[recordKey][ColumnName["status"].value] == "finished":
			self.colorRow(recordKey, "#869191")
			# self.sendFinishedEmail(recordKey)

		elif OverdueTable.isOverdue(self.model.data[recordKey][ColumnName['daterecieved'].value]):
			self.colorRow(recordKey, "#ff1100")

	# def sendFinishedEmail(self, key):
	# 	# need to pull who to send the email to
	# 	self.emailHandler.sendEmail("testuser2020soundsmith@gmail.com", self.model.data[key])

	def createUpdateQuery(self, updatedRows, recordKey):
		query = "update repairconsole set "

		for key in updatedRows:
			query += "`" + ColumnName(key).name + "` = \'%s\'" % (updatedRows[key]) + ","
		query = query[:len(query) - 1] + " where repairnumber = " + str(self.model.getData()[recordKey][ColumnName['repairnumber'].value])
		return query


	def findUpdatedFields(self, recordKey, fields):
		updatedDict = {}
		for key in fields:
			# change to check if is instance of scrolled text THEN if is comments key
			if key == ColumnName['comments'].value:
				comments = fields[key].get("1.0", "end-1c")
				if comments and comments != self.model.getData()[recordKey][key]:
					# change the comment in the field itself when saving
					comment = self.addComment(recordKey, comments)
					updatedDict[key] = comment
			elif key == ColumnName['daterecieved'].value or key == ColumnName['lastupdated'].value:
				if fields[key].get() != self.model.getData()[recordKey][key] and self.isValidDate(fields[key].get()):
					updatedDict[key] = fields[key].get()
			elif key == ColumnName['repairnumber'].value and (int(fields[key].get()) != self.model.getData()[recordKey][key]):
				updatedDict[key] = int(fields[key].get())
			elif key != ColumnName['repairnumber'].value and fields[key].get() != self.model.getData()[recordKey][key]:
				updatedDict[key] = fields[key].get()

		# if updatedDict and not fields[ColumnName['lastupdated'].value].get():
		# if there are any changes, update the "last updated" field
		if updatedDict:
			today = datetime.datetime.today().strftime('%Y-%m-%d')
			updatedDict[ColumnName["lastupdated"].value] = today
		return updatedDict