from tkinter import *
import tkinter as tk

from overdueTable import OverdueTable


class SettingsWidget(object):

	def __init__(self, root=None, **kwargs):
		self.root = root
		self.settings = {}
		self.settingsFile = kwargs.pop("settingFile")
		self.readFromFile()

		# self.createSettingsFrame()

	def readFromFile(self):
		with open(self.settingsFile, "r") as settingFile:
			for line in settingFile:
				lineList = line.split()
				if lineList[-1] == "True" or lineList[-1] == "true":
					self.settings[lineList[0]] = True
				elif lineList[-1] == "False" or lineList[-1] == "false":
					self.settings[lineList[0]] = False
				else:
					self.settings[lineList[0]] = lineList[-1]

		print(self.settings)

	def setRepairTable(self, table):
		self.repairTable = table
		
		# change colors
		self.repairTable.setOverdueColor(self.settings["overdue_color"])
		self.repairTable.setFinishedColor(self.settings["finished_color"])
		self.repairTable.refreshRepairs()

		# change email settings
		self.repairTable.setSendFinishedEmails(self.settings["auto_emails_finish"])

	def setOverdue(self):
		OverdueTable.overdue = int(self.settings["overdue_days"])

	# def getFrame(self):
	# 	return self.settingsFrame

	def writeToFile(self):
		pass

	# def createSettingsFrame(self):
	# 	self.settingsFrame = Frame(self.root)
	# 	self.settingsFrame.pack(side=TOP, fill="both", expand=True)
