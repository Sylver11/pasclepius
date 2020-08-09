function addUniqueClasses(patient_form, treatment_form, search_form = false){
    
    current_patient_form = current_invoice["invoice_id"] + "_current_patient_form";
    current_patient_form = current_patient_form.replace(/\//g, "");
    if(current_invoice["status"] == "draft"){
        patient_form.addEventListener("input", function () {
            keepState(patient_form, treatment_form);
        });
    }
    
    patient_form.classList.add(current_patient_form);
    
    current_form = current_invoice["invoice_id"] + "_current_form";
    current_form = current_form.replace(/\//g, "");
    treatment_form.classList.add(current_form);
    console.log(current_invoice);
    if(current_invoice["status"] == "draft"){
        treatment_form.addEventListener("input", function () {
            keepState(patient_form, treatment_form);
        });
    }
    treatment_form.addEventListener("submit", addSubmit);

    if(search_form){
        current_search_form = current_invoice["invoice_id"] + "_current_search_form";
        current_search_form = current_search_form.replace(/\//g, "");
        search_form.classList.add(current_search_form);
        search_form.addEventListener("keyup", event => {
            if (event.isComposing || event.keyCode === 229) {
                return;
            }
            liveSearch(event)
        })
    }
}