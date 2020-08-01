function populatePatient(){
    var form = document.getElementById("patient_info");
    var invoice_layout = 1;
    for (const [key, value] of Object.entries(current_invoice)) {

        var div = document.createElement("DIV");
        div.className += "form-group ";
        div.className += "row";
        form.appendChild(div);

        var label = document.createElement("Label");
        label.htmlFor = key;
        label.innerHTML= key; 
        label.className = "col-sm-2" 
        label.className += " col-form-label";
        div.appendChild(label);

        var input_div = document.createElement("DIV");
        input_div.className = "col-sm-10"
        div.appendChild(input_div);

        var input = document.createElement("INPUT"); 
        input.value = value;
        input.name = key;
        input.id = key;
        input.disabled = true;
        input.className = "form-control";
        input.setAttribute("type", "text")
        input_div.appendChild(input);

        if(key == "admission_date" || key == "discharge_date" || key == "hospital_name"){
            div.style.display = "none"; 
            div.className += " hospital";
        }
        else if(key == "procedure" || key == "procedure_date" ||key == "diagnosis" || key == "diagnosis_date" || key == "implants" || key == "intra_op" || key == "post_op" ){
            div.style.display = "none"; 
            div.className += " procedure";
        }
        else if(value && key != "csrf_token" && key != "treatments" && key != "date_invoice" && key != "modifier"){
            input.className = "form-control-plaintext";
            var hidden_input = document.createElement("INPUT");
            hidden_input.setAttribute("type", "hidden")
            hidden_input.value = value;
            hidden_input.name = key;
            input_div.appendChild(hidden_input);

            // if(key == "status" || key == "invoice_id" || key == "date_created"){
            //     console.log("soemthing");
            // }   
            if(key == "invoice_layout") {
                invoice_layout = value;
                div.style.display = "none";
            }  
            else if(key == "invoice_file_url" || key == "uuid_text" || key == "id") {
                div.style.display = "none";
            }        
        }
        else{          
            div.style.display = "none"; 
        }                                  
    }

    if(invoice_layout >= 4  && invoice_layout <= 9){
        var hospital = document.getElementsByClassName("hospital");
        for (let i = 0; i < hospital.length; i++) {
        const element = hospital[i];
        element.style.display = "block";  
        input = element.getElementsByTagName("INPUT")[0]
        input.disabled = false; 
        }
        $('#admission_date').datepicker({dateFormat: 'dd.mm.yy'})
        $('#discharge_date').datepicker({dateFormat: 'dd.mm.yy'})
        
    }
    if(invoice_layout >= 7  && invoice_layout <= 12){
        var procedure = document.getElementsByClassName("procedure");
        for (let i = 0; i < procedure.length; i++) {
            const element = procedure[i];
            element.style.display = "block";  
            input = element.getElementsByTagName("INPUT")[0]
            input.disabled = false; 
        }
        $('#procedure_date').datepicker({dateFormat: 'dd.mm.yy'})
    }
}