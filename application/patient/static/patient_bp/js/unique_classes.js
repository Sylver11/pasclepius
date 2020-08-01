function addUniqueClasses(){
    var forms = document.getElementsByTagName('FORM');
    current_form = current_invoice["invoice_id"] + "_current_form";
    current_form = current_form.replace(/\//g, "");
    forms[2].classList.add(current_form);
    forms[2].addEventListener("submit", addSubmit);

    current_patient_form = current_invoice["invoice_id"] + "_current_patient_form";
    current_patient_form = current_patient_form.replace(/\//g, "");
    forms[1].classList.add(current_patient_form);
}