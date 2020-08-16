function firstLetterCapitalise(str) {
    str = str.replace(/_/g, "&nbsp;")
    return str.replace(
        /\w\S*/g,
        function(txt) {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
        }
    );
}



function populatePatient(){
    var form = document.getElementById("patient_info");
    var invoice_layout = 1;

    var form_row_hospitial = document.createElement("DIV");
    form_row_hospitial.className += "form-row ";

    var form_row_procedure_1 = document.createElement("DIV");
    form_row_procedure_1.className += "form-row ";

    var form_row_procedure_2 = document.createElement("DIV");
    form_row_procedure_2.className += "form-row ";

    var form_row_procedure_3 = document.createElement("DIV");
    form_row_procedure_3.className += "form-row ";
   
    for (const [key, value] of Object.entries(current_invoice)) {

        if(key == "admission_date" || key == "discharge_date" || key == "hospital_name"){
            
            var form_group = document.createElement("DIV");
            form_group.className += "form-group ";
            form_group.className += "col-md-4";
            form_group.style.marginBottom = "0";
            form_row_hospitial.appendChild(form_group);

            var label = document.createElement("Label");
            label.htmlFor = key;
            label.innerHTML= firstLetterCapitalise(key); 
            label.className = "col-sm-2" 
            label.className += " col-form-label";
            form_group.appendChild(label);

            var input = document.createElement("INPUT"); 
            input.value = value;
            input.name = key;
            input.id = key;
            input.className = "form-control";
            form_group.appendChild(input);     
        }
        else if(key == "procedure" || key == "procedure_date" ||key == "diagnosis" || key == "diagnosis_date" || key == "implants" || key == "intra_op" || key == "post_op" ){
            
            var form_group = document.createElement("DIV");
            form_group.className += "form-group ";
            form_group.style.marginBottom = "0";

            var label = document.createElement("Label");
            label.htmlFor = key;
            label.innerHTML= firstLetterCapitalise(key);   
            label.className = "col-sm-2" 
            label.className += " col-form-label";
            form_group.appendChild(label);

            var input = document.createElement("INPUT"); 
            input.value = value;
            input.name = key;
            input.id = key;
            input.className = "form-control";
            form_group.appendChild(input);
            

            if(key == "procedure" || key == "procedure_date"){
                
                form_row_procedure_1.appendChild(form_group);
                
                if(key == "procedure"){
                    form_group.className += "col-md-9";
                }
                else{
                    form_group.className += "col-md-3";
                }

            }else if(key == "diagnosis" || key == "diagnosis_date"){
                form_row_procedure_2.appendChild(form_group);
                
                if(key == "diagnosis"){
                    form_group.className += "col-md-9";
                }
                else{
                    form_group.className += "col-md-3";
                }
            }else{
                form_row_procedure_2.appendChild(form_group);
                
                if(key == "implants"){
                    form_group.className += "col-md-6";
                }
                else{
                    form_group.className += "col-md-3";
                }
            }            
        }
        else if(value && key != "csrf_token" && key != "treatments" && key != "date_invoice" && key != "modifier" && key.indexOf(".") === -1){
            var div = document.createElement("DIV");
            div.className += "form-group ";
            div.className += "row";
            div.style.marginBottom = "0";
            form.appendChild(div);

            var label = document.createElement("Label");
            label.htmlFor = key;
            label.innerHTML= firstLetterCapitalise(key);  
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
            
            input.className = "form-control-plaintext";
            input.style.paddingBottom = "0";
            input.style.paddingTop = "0";
            label.style.paddingBottom = "0";
            label.style.paddingTop = "0";
            var hidden_input = document.createElement("INPUT");
            hidden_input.setAttribute("type", "hidden")
            hidden_input.value = value;
            hidden_input.name = key;
            input_div.appendChild(hidden_input);

            if(key == "case_number" || key == "medical_number"){
                var hidden_input = document.createElement("INPUT");
                hidden_input.setAttribute("type", "hidden")
                hidden_input.value = value;
                hidden_input.name = "patient_id";
                input_div.appendChild(hidden_input);

            }

            if(key == "invoice_layout") {
                invoice_layout = value;
                div.style.display = "none";
            }  
            else if(key == "invoice_file_url" || key == "uuid_text" || key == "id") {
                div.style.display = "none";
            }        
        }                                 
    }

    if(invoice_layout >= 4  && invoice_layout <= 9){
        form.appendChild(form_row_hospitial);
        $('#admission_date').datepicker({dateFormat: 'dd.mm.yy'})
        $('#discharge_date').datepicker({dateFormat: 'dd.mm.yy'})      
    }
    if(invoice_layout >= 7  && invoice_layout <= 12){
        form.appendChild(form_row_procedure_1);
        form.appendChild(form_row_procedure_2);
        form.appendChild(form_row_procedure_3);
        $('#procedure_date').datepicker({dateFormat: 'dd.mm.yy'})
        $('#diagnosis_date').datepicker({dateFormat: 'dd.mm.yy'})
    }
}