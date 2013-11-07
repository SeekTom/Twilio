<?php

  require "twilio-php/Services/Twilio.php";

//$mp3 = getRandomMp3();
function getRandomMp3 (){

$files = glob("YourMp3DirectoryHere/*.mp3");
$random = array_rand($files);
$mp3 = $files[$random];

return 'UrlToYourWebsite' .$mp3;
}

$planeUrl = trim(getRandomMp3());
$planeName = str_replace('UrlToYourWebsite', '', $planeUrl);
$planeName = str_replace('.mp3', '', $planeName);
$planeName = str_replace('-', ' ', $planeName);
//echo $plane;
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";

?>

<Response>
<Say voice="female">We miss fleetweek too, so here's something to tide you over to 2014</Say>
<Play><?php echo $planeUrl; ?></Play>
<Sms>Thanks for calling the FleetWeek hotline, you just heard the beautiful sound of <?php echo $planeName; ?>!</Sms>
 
 </Response>