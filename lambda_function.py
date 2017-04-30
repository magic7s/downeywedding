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
	print("Opening Sheet")
	updatesheet = openspreadsheet(os.environ['GSPREAD_FILENAME'], os.environ['GSPREAD_WORKSHEET_WRITE'])
	try:
		print("Looking for number " + str(guestnum).strip("+"))
		guest_confirmation_cell = updatesheet.find(str(guestnum).strip("+"))
		print("Updating cell: " + col + str(guest_confirmation_cell.row))
		message = updatesheet.acell(col + str(guest_confirmation_cell.row)).value + "\n" + message
		updatesheet.update_acell(col + str(guest_confirmation_cell.row), message)
		print("Found number and updated col")
	except gspread.exceptions.CellNotFound:
		newrow = updatesheet.row_count + 1
		updatesheet.insert_row(["", guestnum], index=newrow)
		updatesheet.update_acell(col + str(newrow), message)
		print("Number not found, adding new row")

def handleMMS(event):
	print("Handling MMS")
	message = "Pic URL = " + event['image']
	updatecol(event['fromNumber'], os.environ['GSPREAD_COL_WRITE'], message)
	return message

def handleSMS(event):
	print("Handling SMS")
	message = event['body']
	updatecol(event['fromNumber'], os.environ['GSPREAD_COL_WRITE'], message)
	return message

def lambda_handler(event, context):
    print(event)
#   print (updatesheet.get_all_records())
    try:
        if int(event['numMedia']) > 0:
            handleMMS(event)
        else:    
            handleSMS(event)
        twilio_resp = "Thank you for your response. We look forward to seeing you on August 11th. Check out www.anabrad.com for more info. -- Ana and Brad"
        print("Finished")
        return twilio_resp
    except:
        return("An error occured")