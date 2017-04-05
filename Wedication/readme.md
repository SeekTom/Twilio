# Wedication

This is the barebones of a website/scripts that I used to automate portions of my wedding via SMS:

* initial 'save the date' notifications
* capturing responses from guests to R.S.V.P's
* general notifications (website going live)
* chasing guests for food choices
* statistics on registration/food choices

It uses python, gspread, flask, you'll need to set up a spreadsheet and oAuth stuff in order to be able to poll/update the data, [see here for more details](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)