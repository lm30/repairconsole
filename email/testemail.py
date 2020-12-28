#!/usr/bin/env python3
import smtplib, ssl
port = 465
# 465 for SSL
password = "password@2020"
# password = input("Type email here: ")
context = ssl.create_default_context()

sender_email = "testuser2020soundsmith@gmail.com"
receiver_email = "testuser2020soundsmith@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""

if __name__ == '__main__':
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)