Play random mp3 for caller using twilio
======

This is a simple app for playing an mp3 for a caller - you will need to setup your twilio number and point the Messaging 
Request URL to the sms-reply.php file

You will need to add your mp3's, account sid's etc but the flow is this:

Users texts in a keyword
Twilio calls back and plays a random mp3
Call ends
Twilio texts what the caller just listened to!

