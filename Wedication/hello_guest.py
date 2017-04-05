from flask import Flask,render_template, url_for, request, redirect, make_response
import twilio.twiml
import time
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from datetime import datetime, timedelta

app = Flask(__name__,static_folder='app/static')

json_key = json.load(open('')) #add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
gc = gspread.authorize(credentials)
wks = gc.open("wedding_guests") #add your workbook name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet
wks_food = wks.get_worksheet(1) #food responses worksheet

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')
@app.route("/venue", methods=['GET', 'POST'])
def returnVenue():
    return render_template('venue.html')
@app.route("/food", methods=['GET'])
def returnFood():
    return render_template('food.html')
@app.route("/contact", methods=['GET', 'POST'])
def returnContact():
    return render_template('contact.html')
@app.route("/gifts", methods=['GET', 'POST'])
def returnGifts():
    return render_template('gifts.html')
@app.route("/faq", methods=['GET', 'POST'])
def returnFAQ():
    return render_template('faq.html')
@app.errorhandler(500)
def internal_error(error):
    return "500 error"
    return "!!!!"  + repr(error)
@app.route("/messages", methods=['GET', 'POST'])
def hello_guest():
    
    resp = twilio.twiml.Response() 
    from_number = request.values.get('From', None)
    from_body = request.values.get('Body', None)
    number = from_number
    body_strip = from_body.lower()
    clean_number = number.strip("+")
    
    #all of these values depend on how many guests are at your wedding

    #attendance variables
    guest_confirmed = wks_attendees.acell('C70').value
    guest_unconfirmed = wks_attendees.acell('C71').value
    guest_no_response = wks_attendees.acell('C72').value
    guest_acceptance = wks_attendees.acell('C73').value
    
    #meal total variables
    guest_meals_confirmed = wks_attendees.acell('C78').value 
    guest_meals_unconfirmed = wks_attendees.acell('C79').value
    
    #meal options (name/amount)
    starter_option_1 = wks_food.acell('G2').value
    starter_option_1_amount = wks_food.acell('H2').value
    
    starter_option_2 = wks_food.acell('G3').value
    starter_option_2_amount = wks_food.acell('H3').value

    starter_option_3 = wks_food.acell('G4').value
    starter_option_3_amount = wks_food.acell('H4').value
    
    main_option_1 = wks_food.acell('G5').value
    main_option_1_amount = wks_food.acell('H5').value
    
    main_option_2 = wks_food.acell('G6').value
    main_option_2_amount = wks_food.acell('H6').value
    
    main_option_3 = wks_food.acell('G7').value
    main_option_3_amount = wks_food.acell('H7').value
    
    dessert_option_1 = wks_food.acell('G8').value
    dessert_option_1_amount = wks_food.acell('H8').value
    
    dessert_option_2 = wks_food.acell('G9').value
    dessert_option_2_amount = wks_food.acell('H9').value

    guest_confirmation_cell = wks_attendees.find(str(clean_number).strip()) 
    
    if "yes" in body_strip: 
        #We have a keeper! Find the attendee and update their confirmation_status
        wks_attendees.update_acell("F" + str(guest_confirmation_cell.row), 'Accepted') #update the status to accepted for that guest
        resp.message(u"\u2665" + "Thanks for confirming, we'll be in touch!" + u"\u2665")  #respond to the guest with a confirmation! 
        
    elif "no" in from_body.lower(): #no! 
       #update the confirmation_status row to declined for that guest
        wks_attendees.update_acell("F" + str(guest_confirmation_cell.row), 'Declined')  
        resp.message("Sorry to hear that, we still love you though!") #respond to the user confirming the action 
    
    elif "numbers" in from_body.lower(): #return statistics (total guests, food choices list)   
        resp.message("R.S.V.P update:\n\nTotal Accepted: " + guest_confirmed +
         "\n\nTotal declined: " + guest_unconfirmed + "\n\nTotal no response: " +
        guest_no_response + "\n\nTotal acceptance rate: " + guest_acceptance) 

    elif "food" in body_strip.strip():   #respond with the current food totals and the meal choices  

        resp.message("Guest meals decided:" + guest_meals_confirmed + 
        "\nGuest meals undecided: " + guest_meals_unconfirmed +
        "\n\nMenu breakdown:\n\n" + starter_option_1 +": " +
        starter_option_1_amount + "\n" + starter_option_2 +": " +
        starter_option_2_amount + "\n" + starter_option_3 +": " +
        starter_option_3_amount + "\n" + main_option_1 +": " +
        main_option_1_amount + "\n" + main_option_2 +": " + main_option_2_amount +
        "\n" + main_option_3 +": " + main_option_3_amount + "\n" +
        dessert_option_1 + ": " + dessert_option_1_amount + "\n" + dessert_option_2
        + ": " + dessert_option_2_amount)

    else: #respond with invalid keyword
        resp.message("You sent a different keyword, we need a yes or a no, you sent: " +
        from_body)
    return str(resp)
 
if __name__ == "__main__":
    app.run()