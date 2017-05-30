#!/usr/bin/python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import json
import os
from twilio.rest import Client as TwilioClient

#DEFAULTS
TWILIOSRCNUM = "+13237010811"
def help():
	syntax ="""
	Invalid Syntax
	{cmd} --test|--send templatefile.txt
	""".format(
		cmd=sys.argv[0]
		)
	print(syntax)

def readgooglesheet():
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GSPREAD_OAUTH_FILE'], scope)
	client = gspread.authorize(creds)
	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	myfile = client.open(os.environ['GSPREAD_FILENAME'])
	myworksheet = myfile.worksheet(os.environ['GSPREAD_WORKSHEET_READ'])
	# Extract and print all of the values
	list_of_hashes = myworksheet.get_all_records()
	print json.dumps(list_of_hashes, indent=1)
	return list_of_hashes

def sendsmsout(listofnum, msgbody):
	# Your Account SID from twilio.com/console
	account_sid = os.environ['TWILIO_ACCOUNT_SID']
	# Your Auth Token from twilio.com/console
	auth_token  = os.environ['TWILIO_AUTH_TOKEN']
	client = TwilioClient(account_sid, auth_token)
	for num in listofnum:
		print("Sending to " + str(num))
		message = client.messages.create(
		    to=num, 
		    from_=TWILIOSRCNUM,
		    body=msgbody)
		print(message.sid)	

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return same


##MAIN LOOP##
if len(sys.argv) <= 1:
	print help()
else:
	#Read the template file for filters and message
	smsfile = open(sys.argv[2],"r")
	smstemplate = json.load(smsfile)
	smsfile.close()
	print json.dumps(smstemplate, indent=1)
	#Create a list of persons to send to
	sendto = []
	for person in readgooglesheet():
		if len(smstemplate['filter']) == len(dict_compare(person, smstemplate['filter'])):
			if str(person['Telephone_number']) == '':
				print("Skipping " + str(person['Name']) + " due to missing number")
				continue
			sendto.append("+" + str(person['Telephone_number']))
	#Do we test or send?
	if sys.argv[1] == "--send":
		sendsmsout(sendto,smstemplate['message'])
	elif sys.argv[1] == "--test":
		print("THIS IS ONLY A TEST\nSending to:")
		print(sendto)
		print("Message:")
		print(smstemplate['message'])
	else:
		print help()
	