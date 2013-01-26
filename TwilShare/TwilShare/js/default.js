// For an introduction to the Blank template, see the following documentation:
// http://go.microsoft.com/fwlink/?LinkId=232509
(function () {
    "use strict";

    WinJS.Binding.optimizeBindingReferences = true;

    var app = WinJS.Application;
    var activation = Windows.ApplicationModel.Activation;
    var shareOperation;

    app.onactivated = function (args) {
        if (args.detail.kind === activation.ActivationKind.launch) {
            if (args.detail.previousExecutionState !== activation.ApplicationExecutionState.terminated) {
                // TODO: This application has been newly launched. Initialize
                // your application here.
                headerLBL.textContent = "started";

                var oRequestDB = window.indexedDB.open("Messages", 1);
                
                oRequestDB.onsuccess = function (event) {
                    db1 = oRequestDB.result;

                    if (db1.version == 1) {

                        txn = db1.transaction(["Message"], IDBTransaction.READ_ONLY);
                        var objStoreReq = txn.objStore("Message");
                        var request = objStoreReq.get("Message0");
                        request.onsuccess = processGet;
                    }
               

                };
            

                document.getElementById("confirmButton").addEventListener("click", confirmOrder, false);
                btnSend.addEventListener("click", sendButtonClick);
                var dataTransferManager = Windows.ApplicationModel.DataTransfer.DataTransferManager.getForCurrentView();
                dataTransferManager.addEventListener("datarequested", shareTextHandler);

            }
        }
        else if (args.detail.kind === activation.ActivationKind.shareTarget) {
            //app is launched as a sharetarget..
            // Code to handle activation goes here.
            headerLBL.textContent = "share";
            shareOperation = args.detail.shareOperation;
            //We receive the ShareOperation object as part of the eventArgs.
            shareOperation = args.detail.shareOperation;

            // We queue an asychronous event so that working with the ShareOperation object 
            // does not block or delay the return of the activation handler.
            WinJS.Application.addEventListener("shareready", shareReady, false);
            WinJS.Application.queueEvent({ type: "shareready" });
        } else {
            headerLBL.textContent = "resume";

            // TODO: This application has been reactivated from suspension.
            // Restore application state here.
        }
     //   document.getElementById("btnSend").addEventListener("click", showConfirmFlyout, false);
       
        args.setPromise(WinJS.UI.processAll());

    };


    function showConfirmFlyout() {
        showFlyout(errorFlyout, btnSend, "top");
    }
    function showFlyout(flyout, anchor, placement) {
        flyout.winControl.show(anchor, placement);
    }
    function confirmOrder() {
        document.getElementById("errorFlyout").winControl.hide();
    }


   

 function shareReady(args) {
    if (shareOperation.data.contains(Windows.ApplicationModel.DataTransfer.StandardDataFormats.text)) {
        shareOperation.data.getTextAsync().done(function (textValue) {
            // To output the text using this example, you need a div tag with an 
            // id of "output" in your HTML file.
         //   document.getElementById("output").innerText = textValue;
            document.getElementById("bx_message").innerText = textValue;
        });
    }
}

   

    function shareTextHandler(e) {
        var request = e.request;
        request.data.properties.title = "Share text message";
        request.data.properties.description = "Share message content";
        request.data.setText(document.getElementById(bx_message.innerText   ));
    }

    function sendButtonClick(e) {
        var accountSid = "ACbb74cfe31aba46d9a358fb94d6a3bcfb";
        var authKey = "72a7ee6e57367f14d30c674bee069ab4";
        var resMessage = document.getElementById("bx_message").value;
        var messageString = "Sending message: " + resMessage + " to number: "+bx_number.value;
        document.getElementById("msgResponse").innerText = messageString;
        var dataStr = "From=+442033224624&To="+ bx_number.value + " &Body=" + resMessage;
        //var dataStr = "From=+44 7737088306&To=" + bx_number.value + " &Body=" + resMessage;

        WinJS.xhr({
            type: "post", user: accountSid, password: authKey,
            url: "https://api.twilio.com/2010-04-01/Accounts/" + accountSid + "/SMS/Messages.xml",
            headers: { "Content-type": "application/x-www-form-urlencoded" },
            data: dataStr
        }).then(
  function (success) {
      //message sent!
      document.getElementById("errorContent").innerText = "Message sent!";
      showConfirmFlyout();
  },
  function (error) {
      //message sent!
      document.getElementById("errorContent").innerText = "Message not sent!";
      showConfirmFlyout();
    //  msgProgrss.innerText = "Message has not sent :(";
  }
);

    }
    app.oncheckpoint = function (args) {
        // TODO: This application is about to be suspended. Save any state
        // that needs to persist across suspensions here. You might use the
        // WinJS.Application.sessionState object, which is automatically
        // saved and restored across suspension. If you need to complete an
        // asynchronous operation before your application is suspended, call
        // args.setPromise().
    };

    app.start();
})();
