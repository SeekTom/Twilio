Twilio Windows Store share app
======

This is a simple example app using the Twilio API, its uses Javascript/HTML5

It should work out of the box after you've added your AID and SID to this function:

 function sendButtonClick(e) {
        var accountSid = ""; //Add SID
        var authKey = ""; //Add AID
  	var numSend = "";// Add your Twilio number
        var resMessage = document.getElementById("bx_message").value;
        var messageString = "Sending message: " + resMessage + " to number: "+bx_number.value;
        document.getElementById("msgResponse").innerText = messageString;
        var dataStr = "From="+ numSend +"&To="+ bx_number.value + " &Body=" + resMessage;
        //var dataStr = "From=+44 7737088306&To=" + bx_number.value + " &Body=" + resMessage;

        WinJS.xhr({
            type: "post", user: accountSid, password: authKey,
            url: "https://api.twilio.com/2010-04-01/Accounts/" + accountSid + "/SMS/Messages.xml",
            headers: { "Content-type": "application/x-www-form-urlencoded" },
            data: dataStr
        })
