<?php
 header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1

  require "twilio-php/Services/Twilio.php";
 
    // make an associative array of senders we know, indexed by phone number
   
   $from_number = $_REQUEST['From'];
   $sms_body = $_REQUEST['Body'];

  $AccountSid = "";
  $AuthToken = "";
 
    // Step 3: instantiate a new Twilio Rest Client
 $client = new Services_Twilio($AccountSid, $AuthToken);
 
 $trimmed_sms_body = str_replace(' ', '', strtolower($sms_body));

 if  (strpos($trimmed_sms_body,'YourKeyWordhere') !== false) {
  //We got a music fan on our hands, lets celebrate

   $client->account->messages->sendMessage('YourTwilioNumberhere', $from_number, 'Missing YourKeyWordhere? I have something that just might help with that!');
   $client->account->calls->create('YourTwilioNumberhere', $from_number, 'files.php', array());
  }

else 
{
   $client->account->messages->sendMessage('YourTwilioNumberhere', $from_number, 'Psst the keyword is YourKeyWordhere! You sent: ' .$trimmed_sms_body);
   //Wrong keyword, bad user!
}



?>

