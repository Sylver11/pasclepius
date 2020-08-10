function addShow(data) {
    for (const [key, value] of Object.entries(data)) {
        var message = document.getElementById("result")
        var status = document.createElement("P"); 
        status.innerHTML = key + ": " + value          
        message.appendChild(status)
        if(key == "swriter_status"){
            if(value == "Success"){
                var download_button = document.getElementById("download_invoice")
                download_button.style.display = "block"
                download_button.disabled = false;
            }
        }
    }
}


function addSubmit(ev) {
    if(document.getElementById('method').checked){
        var form = document.getElementById("patient_info") 
        inputs = form.getElementsByTagName("input")
        for(var i = 0, len = inputs.length; i < len; i++) {
            input = inputs[i];
            if(!input.value && input.disabled != true) {
                ev.preventDefault();
                input.focus();
                input.style.borderColor = "red";
                alert("When creating an invoice file all fields must be filled out :)");
                return;
            }
        }
    }
    ev.preventDefault();
    var submit = document.getElementById("submit");
    submit.disabled = true;
    submit.innerHTML = "Saving... "
    var span = document.createElement("SPAN");
    span.className = "spinner-border"; 
    span.className +=  " spinner-border-sm";
    span.setAttribute("role", "status");
    span.setAttribute("aria-hidden", "true");
    submit.appendChild(span);
    $.ajax({
        method: 'POST',
        url: '/patient/invoice/generate',
        data: $('.' + current_form).serialize()+ "&" + $("." + current_patient_form).serialize(),
        success: function (data) {
            data = JSON.parse(data);
            if(data){
                var forms = document.getElementsByTagName('FORM');
                for (let i = 1; i < forms.length; i++) {
                    let form = forms[i];
                    var inputs = form.getElementsByTagName("input")          
                    for(let x = 0; x < inputs.length; x++) {
                        var input = inputs[x];
                        input.disabled = true;
                    } 
                    var selects = form.getElementsByTagName("select")
                    for(let x = 0; x < selects.length; x++) {
                        var select = selects[x];
                        select.disabled = true;
                    }      
                }  
                if(current_invoice['status'] == "draft"){
                    var tab_draft = document.getElementById("tab-draft");
                    tab_draft.innerHTML = data['invoice_id']
                    tab_draft.disabled = true;
                }
                span.remove();
                submit.innerHTML = "Saved"
                addShow(data); 
            }   
        },
        error: function(xhr, status, error){
            var errorMessage = xhr.status + ': ' + xhr.statusText;
            alert('Error - ' + errorMessage);
        }
    })
}


