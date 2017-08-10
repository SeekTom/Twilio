import json
import time
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from twilio.rest  import Client

#Message your attendees from a spreadsheet

json_key = json.load(open('.json'))#add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
wks = gc.open("wedding_guests") #add your workbook name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet

ACCOUNT_SID = os.environ['Twilio_account_per']
AUTH_TOKEN = os.environ['Twilio_account_token_per'] 

client = Client(ACCOUNT_SID, AUTH_TOKEN) 
     
for num in range(2,60):  #to iterate between guests, amend this based on your total
    print "sleeping for 2 seconds"
    time.sleep(2) #adding a delay to avoid filtering
    
    guest_number = wks_attendees.acell('B' +str(num)).value
    guest_name = wks_attendees.acell('A'+str(num)).value
    
    if not  guest_number:
        print guest_name + ' telephone number empty not messaging'
        wks_attendees.update_acell('E'+str(num), '0') #set number to 0
    
    else:
        print  'Sending message to ' + guest_name
        client.messages.create(
            to="+" + guest_number, 
            from_="", #your twilio number here
            body= u"\u2B50" + u"\u2764" + u"\u2B50" + u"\u2764" + u"\u2B50" + u"\u2764" + u"\u2B50" + u"\u2764" + "\n\n" + u"\u2709" +" Save the date! "+ u"\u2709" +"\n\nLauren Pang and Thomas Curtis are delighted to invite you to our wedding.\n\nSaturday 3rd September 2016. \n\nColville Hall,\nChelmsford Road,\nWhite Roding,\nCM6 1RQ.\n\nThe Ceremony begins at 2pm.\n\nMore details will follow shortly!\n\nPlease text YES if you are saving the date and can join us or text NO if sadly, you won't be able to be with us.\n\n" u"\u2B50" + u"\u2764" + u"\u2B50" + u"\u2764" + u"\u2B50" + u"\u2764" + u"\u2B50" + u"\u2764",  
            #body ="Hello you lovely people, tomorrow is the big day!!\n\nPost code for the venue: CM6 1RQ\n\nArrival time one thirty for a two o'clock ceremony.\n\nIt is a cash bar, so please bring sufficient money with you as there is no nearby cash machine.\n\nIt might be raining at some point in the day, so an umbrella might be required.\n\nThe venue is non smoking, due to the thatched buildings.\n\nWe could not be more excited that you are joining us for our special day and looking forward to sharing great food and good times!\n\nTom & Lauren",
        )
        wks_attendees.update_acell('E'+str(num), int(wks_attendees.acell('E' +str(num)).value) + 1) #increment the message count row
else:                  # else part of the loop
   print 'finished'
