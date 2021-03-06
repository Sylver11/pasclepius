function addShow(data) {
    var save_message;
    var save_type;
    if (data["db_status"] == "Success"){
        save_message = "Success"
        save_type = "success"      
    }
    else{
        save_message = "Failed"
        save_type = "danger" 
    }
    $.notify({
        icon:"glyphicon glyphicon-warning-sign",
        title: "<strong> " + save_message + " </strong>",
        message: data["db_description"]
    },{
        placement: {
            from: "top",
            align: "right"
        },
        type: save_type,
        delay: 10000,
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        }
    });
    var swriter_message;
    var swriter_type;
    if(data["swriter_status"]){
        if (data["swriter_status"] == "Success"){
            swriter_message = "Success";
            swriter_type = "success";
            var show_invoice_button = document.getElementById("show_invoice")
            show_invoice_button.setAttribute("href",data["nextcloud_domain_full"] + "/index.php/f/" + data["invoice_file_id"])
            show_invoice_button.setAttribute("target","_blank")
            show_invoice_button.style.display = "block"
            show_invoice_button.disabled = false;
            show_invoice_button.className += " active";
        }
        else {
            swriter_message = "Failed";
            swriter_type = "danger";
        }
        $.notify({
            icon:"glyphicon glyphicon-warning-sign",
            title: "<strong> " + swriter_message + " </strong>",
            message: data["swriter_description"]
        },{
            placement: {
                from: "top",
                align: "right"
            },
            type: swriter_type,
            delay: 10000,
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutUp'
            }
        });
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
                    var tab_draft = document.getElementById("tab-draft-button");
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


