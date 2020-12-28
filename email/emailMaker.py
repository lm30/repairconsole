class EmailMaker(object):
	def __init__(self, messageFile, senderEmailFile):
		self.senderEmailFile = senderEmailFile
		self.messageFile = messageFile
		self.emailData = {}
		self.setup()

	def setup(self):
		self.loadSenderEmailFile()
		self.loadMessage()

	def loadSenderEmailFile(self):
		with open(self.senderEmailFile, "r") as senderFile:
			for line in senderFile:
				lineList = line.split()
				self.emailData[lineList[0]] = lineList[-1]

	def loadMessage(self):
		with open(self.messageFile, "r") as message:
			self.emailData["message"] = message.read()

	def sendEmail(self, receiverEmail, fillIn):
		pass

	def sendEmails(self, receiverEmailList):
		pass