from tkinter import *
import tkinter as tk
import datetime
import mysql.connector as mysql

from editWidget import EditWidget

class AddItemWindow(EditWidget):

	def createWidget(self):
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
		self.table.redraw()
		self.table.sortTable(columnName="repairnumber")

		query, valuesList = self.createAddQuery(addedItems)
		self.updateDatabase(query, values=valuesList)

		window.destroy()

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
