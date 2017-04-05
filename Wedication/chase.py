import json
import time
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from twilio.rest  import TwilioRestClient

json_key = json.load(open('')) #json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
wks = gc.open("") #add your spreadsheet name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet

ACCOUNT_SID = os.environ['Twilio_account_per']
AUTH_TOKEN = os.environ['Twilio_account_token_per'] 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
     
for num in range(2,72):  #manual hack to ensure no guests not left out
    print "sleeping for 3 seconds"
   
    time.sleep(3) #adding a delay to avoid carrier filtering
    wedding_guest_number = wks_attendees.acell('B' +str(num)).value #grab the attendee number 
    wedding_guest_name = wks_attendees.acell('A'+str(num)).value #
    
    menu_guest = wks_attendees.acell('G' +str(num)).value

    if not wedding_guest_number:
        
        print wedding_guest_name + ' telephone number empty not messaging' #output to console that we are not messaging this guest due to lack of telephone number
        wks_attendees.update_acell('H'+str(num), '1') #increment the message count row for the individual user
    
    else:
        if menu_guest == "N": #guest has not chosen food! CHASE THEM!
            print  'Sending message to ' + wedding_guest_name
            client.messages.create(
                to="+" + wedding_guest_number, 
                from_="", #your Twilio number here 
                body ="If you have received this message, you have not chosen your food options for Tom & Lauren's Wedding!\n\nYou can pick your choices via the website, no paper or postage required!\n\nhttp://www.tomlauren2016.com/food"
            )
            wks_attendees.update_acell('H'+str(num), int(wks_attendees.acell('H' +str(num)).value) +1) #increment the message count row for the individual user
else:                  # else part of the loop
   print 'finished'