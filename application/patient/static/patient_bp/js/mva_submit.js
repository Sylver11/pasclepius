$('.mva').submit(function (e) {
    if (!$(".save_patient").is(":checked")){
        var x = document.forms["mva"]["tariff"].value; 
        if (x == "") {
            e.preventDefault();
            alert("Tariff must be chosen.");
            return
        }
    }
        e.preventDefault();
        $.post( "/patient/invoice/new", $('.mva').serialize(), function( data ) {
            $( "#invoice-tab" ).html( data );
            var lower_navbar = document.getElementById("navbarTogglerDemo01")
            var tabs = lower_navbar.getElementsByTagName('BUTTON');
            for (var i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove("active");
            }
            $('.invoices').removeClass('active');
            $('.new-patient').removeClass('active'); 
            var draft_button = document.createElement("BUTTON");  
            draft_button.setAttribute("id", "tab-draft-button")
            draft_button.setAttribute("class", "btn btn-secondary my-2 my-lg-0 tab-draft-button active")
            draft_button.textContent = "Draft";
            draft_button.addEventListener("click", function(e){ 
                e.preventDefault();
                var tabs = lower_navbar.getElementsByTagName('BUTTON');
                for (var i = 0; i < tabs.length; i++) {
                    tabs[i].classList.remove("active");
                }
                $('.invoices').removeClass('active');
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
            favi.setAttribute("id" , "draft_delete_favi");
            favi.setAttribute("class" , "fa fa-remove favi mr-sm-2 ml-2");
            favi.addEventListener("click", function(e){
                e.preventDefault();
                $.ajax({
                    type: "GET",
                    url: '/remove-job', 
                    data: {work_type: "invoice_draft", work_quality: "any"},
                    success: function (status) {
                        tab_to_be_removed = document.getElementById("tab-draft");
                        tab_to_be_removed.remove();
                    },
                    error: function(xhr, status, error){
                        var errorMessage = xhr.status + ': ' + xhr.statusText;
                        alert('Error - ' + errorMessage);
                    }
                }) 
            });


            var draft_tab_wrapper = document.createElement("FORM");
            draft_tab_wrapper.setAttribute("id", "tab-draft");
            draft_tab_wrapper.setAttribute("class", "form-inline");           
            draft_tab_wrapper.appendChild(draft_button);
            draft_tab_wrapper.appendChild(favi);

            if(document.getElementById("tab-draft")){
                lower_navbar.replaceChild(draft_tab_wrapper, document.getElementById("tab-draft"));
            }
            else{
                var referenceNode = document.getElementById("tab-0")
                lower_navbar.insertBefore(draft_tab_wrapper, referenceNode)
            }         
        })
        .fail(function(xhr, status, error) {
            var errorMessage = xhr.status + ': ' + xhr.statusText;
            alert('Error - ' + errorMessage);
        })
});