import smtplib, ssl

# from emailMaker import EmailMaker
from emailCreator.emailMaker import EmailMaker

class EmailSMTPMaker(EmailMaker):
	def __init__(self, messageFile, senderEmailFile):
		super(EmailSMTPMaker, self).__init__(messageFile, senderEmailFile)
		self.emailData["port"] = 465

	def sendEmail(self, receiverEmail, fillIn):
		pass
		# receiverEmailList = {receiverEmail: fillIn}
		# self.sendEmails(receiverEmailList)

	def sendEmails(self, receiverEmailList):
		try:
			context = ssl.create_default_context()
			with smtplib.SMTP_SSL("smtp.gmail.com", self.emailData["port"], context=context) as server:
				server.login(self.emailData['email'], self.emailData['password'])
				for receiverEmail in receiverEmailList:
					server.sendmail(
						self.emailData['email'],
						receiverEmail,
						self.emailData['message'].format(**receiverEmailList[receiverEmail])
					)
		except:
			print("Unable to send email")


# testEmail = EmailSMTPMaker("emailTemplates/overdueMessage.txt", "emailInfo/testuser2020soundsmith.txt")
# testEmail = EmailSMTPMaker("emailCreator/emailTemplates/overdueMessage.txt", "emailCreator/emailInfo/testuser2020soundsmith.txt")
# print("Starting...")
# testEmail = EmailSMTPMaker("emailTemplates/overdueMessage.txt", "emailInfo/testuser2020soundsmith.txt", {"testuser2020soundsmith@gmail.com": {"First name": "PersonName", "Repair number": "12345", "Date recieved": "10/12/2020" , "Last updated": "12/12/2020", "Repaired by": "Person"}})

# testEmail.sendEmail("testuser2020soundsmith@gmail.com", {"First name": "PersonName", "Repair number": "12345", "Date recieved": "10/12/2020" , "Last updated": "12/12/2020", "Repaired by": "Person"})

# testEmail.sendEmail("testuser2020soundsmith@gmail.com", {"First name": "PersonName", "Repair number": "12345", "Date recieved": "10/12/2020" , "Last updated": "12/12/2020", "Repaired by": "Person"})
# testEmail.sendEmail("testuser2020soundsmith@gmail.com", {"First name": "PersonName", "Repair number": "12345", "Date recieved": "10/12/2020" , "Last updated": "12/12/2020", "Repaired by": "Person"})
# testEmail.sendEmail("testuser2020soundsmith@gmail.com", {"First name": "PersonName", "Repair number": "12345", "Date recieved": "10/12/2020" , "Last updated": "12/12/2020", "Repaired by": "Person"})
# testEmail.sendEmails({"testuser2020soundsmith@gmail.com": {"name": "PersonName", "repairnumber": "12345", "lastupdated": "12/12/2020"}})
