import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('DowneyWeddingAPI-871ef8dec0dc.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
myfile = client.open("Downey Wedding 8/11/17: All-in-One Wedding Planner")
myworksheet = myfile.worksheet('SMS')

# Extract and print all of the values
list_of_hashes = myworksheet.get_all_records()
print(list_of_hashes)
for people in list_of_hashes:
	print(people['Name'] + "-->" + str(people['Telephone_number']))

guest_confirmation_cell = myworksheet.find(str('19254573000').strip())
count = myworksheet.acell("D" + str(guest_confirmation_cell.row))
print(int(count.value) + 1)
myworksheet.update_acell("D" + str(guest_confirmation_cell.row), int(count.value) + 1) 
	

