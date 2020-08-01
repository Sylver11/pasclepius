function keepState(patient_form, treatment_form){
    var data = serializeArray(patient_form).concat(serializeArray(treatment_form))
    current_invoice = {};
    var treatments = [];
    var obj = {};
    var counter = 0; 
    if(data != 'undefined' && data.length !== 0){
        if(data[2]["value"] != ""){
            $.each(data, function(){
                if(this.name == "treatments" || this.name == "description" || this.name == "date" || this.name == "value" || this.name == "post_value" || this.name == "units"){
                obj[this.name] = this.value
                counter++;
                    if(counter == 6){
                        treatments.push(obj);
                        obj = {};
                        counter = 0;
                    }      
                }
                else{
                current_invoice[this.name] = this.value;
                }
            })
            current_invoice["treatments"] = treatments;
            var invoice_json_string = JSON.stringify(current_invoice);
            var url = "/add-job";
            $.ajax({
                type: "GET",
                url: url,
                data: {work_quality: invoice_json_string, work_type: 'invoice_draft'},
                success: function () {
                }
            });
        }   
    }  
}