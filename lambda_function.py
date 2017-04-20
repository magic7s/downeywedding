'''
Twilio handler function to receive replys from txt sent
'''
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def openspreadsheet(file, sheet):
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GSPREAD_OAUTH_FILE'], scope)
	# Need to add error handle here
	client = gspread.authorize(creds)
	myfile = client.open(file)
	myworksheet = myfile.worksheet(sheet)
	return myworksheet

def updatecol(guestnum, col, message):
	updatesheet = openspreadsheet(os.environ['GSPREAD_FILENAME'], os.environ['GSPREAD_WORKSHEET_WRITE'])
	guest_confirmation_cell = updatesheet.find(str(guestnum).strip("+"))
	# If find fails insert a new row
	updatesheet.update_acell(col + str(guest_confirmation_cell.row), message) 

def handleMMS(event):
	message = "Pic URL = " + event['image']
	updatecol(event['fromNumber'], os.environ['GSPREAD_COL_WRITE'], message)
	return message

def handleSMS(event):
	message = event['body']
	updatecol(event['fromNumber'], os.environ['GSPREAD_COL_WRITE'], message)
	return message

def lambda_handler(event, context):
    print(event)
#   print (updatesheet.get_all_records())
    if int(event['numMedia']) > 0:
        twilio_resp = handleMMS(event)
    else:    
        twilio_resp = handleSMS(event)
    twilio_resp = "Thank you for your response. --Ana & Brad"
    return twilio_resp
