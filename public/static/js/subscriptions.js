// Subscribe for newsletter

$(document).ready(function() {

    // Add Email to subscriptions
    $('form#subscribeNow').on('submit', function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();

        console.log("Form for subscribe");

        let email = $(this),
            data = {};
        data['email'] = email.find("input#emailAdress").val();        

        $.ajax({
            method: email.attr("method"),
            url: email.attr("action"),
            data: data,
            success: function(res){
                let form = $("form#subscribeNow").addClass("d-none");
                let mess = $("#subscriptionMessage").removeClass('d-none').text(res.message);    
                setTimeout(function(){
                    mess.addClass("d-none");
                    form.find("input#emailAdress").val("");
                    form.removeClass("d-none");
                }, 2500)    
           },
            error: function(err){  }
        })

    }); // End

});