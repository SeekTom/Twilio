import json
import time
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from twilio.rest  import Client

json_key = json.load(open('')) #add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
wks = gc.open("") #add your spreadsheet name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet
wks_food = wks.get_worksheet(1) #foodresponses worksheet

ACCOUNT_SID = os.environ['Twilio_account_per']
AUTH_TOKEN = os.environ['Twilio_account_token_per'] 

client = Client(ACCOUNT_SID, AUTH_TOKEN) 
     
for num in range(2,60):  #to iterate between 10 to 60 manual hack to ensure no guests not left out
    
  val_food_guest_name = wks_food.acell('B' +str(num)).value #food choice name column
     
  if val_food_guest_name:
    val_attendees_name = wks_attendees.find(val_food_guest_name).value
    val_attendees_name_row = wks_attendees.find(val_food_guest_name).row
    val_menu_status = wks_attendees.acell("G" + str(val_attendees_name_row)).value
    guest_meals_confirmed = wks_attendees.acell('C78').value 
    guest_meals_unconfirmed = wks_attendees.acell('C79').value
    
    if val_food_guest_name == val_attendees_name: 
          print 
          if val_menu_status == 'Y': #data already matched, move on
           print('Skipping') 
          
          else: #user has supplied their choices, update main spreadsheet
            print ('Food sheet name ' + val_food_guest_name + 'Attendees sheet name ' + val_attendees_name)
            #update menu choices row
            wks_attendees.update_acell("G" + str(attendees_name_row), 'Y')
    else:
      print('nothing found, moving on')
      wks_attendees.update_acell('E'+str(num), int(wks.acell('E' +str(num)).value) + 1) #increment the message count row

  else:
    #send message to the admin that the process has been completed with update stats
    client.messages.create(
    from_="", #twilio number here 
    to="", #admin number here  
    body ="Finished processing current meal list\n\nGuest meals confirmed" + guest_meals_confirmed + "\n\nGuest meals unconfirmed: " + guest_meals_unconfirmed)

