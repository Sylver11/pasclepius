function isValidDate(dateString){
    if(!/^\d{4}\-\d{1,2}\-\d{1,2}$/.test(dateString))
        return false;
    var parts = dateString.split("-");
    var day = parseInt(parts[2], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[0], 10);
    if(year < 1000 || year > 3000 || month == 0 || month > 12)
        return false;
    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];
    if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
        monthLength[1] = 29;
    return day > 0 && day <= monthLength[month - 1];
};



$('.other').submit(function (e) {
    if (!$(".save_patient").is(":checked")){
        var x = document.forms["other"]["tariff"].value; 
        if (x == "") {
            e.preventDefault();
            alert("Tariff must be chosen.");
            return
        }
    }

    var y = document.forms["other"]["patient_birth_date"].value;
    if(isValidDate(y)){
        e.preventDefault();
        $.post( "/patient/invoice/new", $('.other').serialize(), function( data ) {
            $( "#invoice-tab" ).html( data );
            var lower_navbar = document.getElementById("myTab")
            var draft_button = document.createElement("BUTTON");  
            draft_button.setAttribute("id", "tab-draft");
            draft_button.className += " btn";
            draft_button.className += " btn-secondary "
            draft_button.className += " btn-sm "
            draft_button.style.marginLeft = "2em";
            draft_button.textContent = "Draft";
            draft_button.addEventListener("click", function(e){ 
                e.preventDefault();
                var tabs = lower_navbar.getElementsByTagName('BUTTON');
                for (var i = 0; i < tabs.length; i++) {
                    tabs[i].classList.remove("active");
                }
                $('.continue').removeClass('active');
                $('.new-patient').removeClass('active'); 
                $(this).addClass('active'); 

                $.ajax({
                    type: "GET",
                    url: '/patient/last-five', 
                    data: {work_type: "invoice_draft"},
                    success: function (patient) {
                        patient = JSON.parse(patient);
                        patient = JSON.parse(patient[0]["work_quality"].replace(/\\"/g, '"'));
                        $.get( "/patient/invoice/new", {"tariff": patient["tariff"], "status": "continue_draft"}, function( data ) {
                            $( "#invoice-tab" ).html( data );
                        });
                    },
                    error: function(xhr, status, error){
                        var errorMessage = xhr.status + ': ' + xhr.statusText;
                        alert('Error - ' + errorMessage);
                    }
                })
            }, false);

            var favi = document.createElement("I");
            favi.setAttribute("class" , "fa fa-remove")
            favi.setAttribute("id" , "draft_delete_favi")
            favi.style.paddingLeft ="5px";
            favi.addEventListener("click", function(e){
                e.preventDefault();
                $.ajax({
                    type: "GET",
                    url: '/remove-job', 
                    data: {work_type: "invoice_draft", work_quality: "any"},
                    success: function (status) {
                        favi_to_be_removed = document.getElementById("draft_delete_favi");
                        favi_to_be_removed.remove();
                        tab_to_be_removed = document.getElementById("tab-draft");
                        tab_to_be_removed.remove();
                    },
                    error: function(xhr, status, error){
                        var errorMessage = xhr.status + ': ' + xhr.statusText;
                        alert('Error - ' + errorMessage);
                    }
                }) 
            });

            if(document.getElementById("tab-draft")){
                lower_navbar.replaceChild(draft_button, document.getElementById("tab-draft"));
            }
            else{
                var referenceNode = document.getElementById("tab-0")
                lower_navbar.insertBefore(draft_button, referenceNode)
                lower_navbar.insertBefore(favi, referenceNode)
            }
        })
        .fail(function(xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText;
            alert('Error - ' + errorMessage);
        })
    } 
    else{
        e.preventDefault();
        alert("Patient birth date has an incorrect format. Please use the following format: yyyy-mm-dd");
    } 
});


var other_medical_aid_field = document.querySelector('.other_medical_aid');
other_medical_aid_field.addEventListener('keypress', function ( e ) {  
    var key = e.keyCode;
    if (key === 32) {
        e.preventDefault();
        alert("No whitespace please :)");
    }
});