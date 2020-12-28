import smtplib, ssl

from emailMaker import EmailMaker

class EmailSMTPMaker(EmailMaker):
	def __init__(self, messageFile, senderEmailFile):
		super(EmailSMTPMaker, self).__init__(messageFile, senderEmailFile)
		self.emailData["port"] = 465

	def sendEmail(self, receiverEmail, fillIn):
		self.sendEmails({receiverEmail: fillIn})

	def sendEmails(self, receiverEmailList):
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL("smtp.gmail.com", self.emailData["port"], context=context) as server:
			server.login(self.emailData['email'], self.emailData['password'])
			for receiverEmail in receiverEmailList:
				server.sendmail(
					self.emailData['email'],
					receiverEmail,
					self.emailData['message'].format(**receiverEmailList[receiverEmail])
				)


testEmail = EmailSMTPMaker("email/emailTemplates/overdueMessage.txt", "email/emailInfo/testuser2020soundsmith.txt")
testEmail.sendEmail("testuser2020soundsmith@gmail.com", {"name": "PersonName", "repairnumber": "12345", "lastupdated": "12/12/2020"})
# testEmail.sendEmails({"testuser2020soundsmith@gmail.com": {"name": "PersonName", "repairnumber": "12345", "lastupdated": "12/12/2020"}})
