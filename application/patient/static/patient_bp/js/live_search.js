function removeActive(x) {
    for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
        }
    }   

function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("autocomplete-active");
}

function uniq_fast(a) {
    var seen = {};
    var out = [];
    var len = a.length;
    var j = 0;
    for(var i = 0; i < len; i++) {
        var item = a[i];
        if(seen[item] !== 1) {
            seen[item] = 1;
            out[j++] = item;
            }
        }
    return out;
}

function liveSearch (e) {     

    e.preventDefault();
    var key = e.keyCode || e.which;
    if((key === 38 || key === 40) && !e.shiftKey && !e.metaKey && !e.ctrlKey && !e.altKey){
        console.log("aarro key pressed ");
        /////////////////////////////////////////////
        //TODO add func for skipping the list down using arrow keys
        /////////////////////////////////////////////
    }
    var currentFocus;
    var input_element = document.getElementById("treatmentsearch")
    var url = "/live-search-treatment";
    var a, b, i, val = input_element.value;
    var search_item = input_element.value

    $.ajax({
        type: "GET",
        url: url,
        data: {treatment: search_item, tariff: current_invoice["tariff"]}, 
        dataType: 'json',
        success: function (returnData) {
            if (returnData.treatments.length <= 20){
            var names = [], range = returnData.treatments.length;
            }
            else{
            var names = [], range = 10
            }
            for (i = 0; i < range; i++) {
                names[i] = returnData.treatments[i]['description']
            }


            if (returnData.items.length <= 9){
            var items = [], range = returnData.items.length;
            }
            else{
            var items = [], range = 10
            }
            for (i = 0; i < range; i++) {
                items[i] = returnData.items[i]['item'].toString()
            }
            
            closeAllLists();
            if (!val) { return false;}
            currentFocus = -1;
            var a = document.createElement("DIV");
            a.setAttribute("id", "autocomplete-list2");
            a.setAttribute("class", "autocomplete-items2");
            input_element.parentNode.insertBefore(a, input_element.nextSibling);
            for (z = 0; z < items.length; z++) {
                if (items[z].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                    var b = document.createElement("DIV");
                    var wrapper_b = document.createElement("DIV");
                    b.setAttribute('class','treatment-divs')
                    b.style.cursor = "pointer";
                    wrapper_b.style.display = "flex";
                    wrapper_b.style.justifyContent = "flex-start";
                    wrapper_b.style.alignItems = "center";
                    var category = returnData.items[z]['category'];
                    var sub_category = returnData.items[z]['sub_category'];
                    var sub_sub_category = returnData.items[z]['sub_sub_category']
                    var sub_sub_sub_category = returnData.items[z]['sub_sub_sub_category']
                    var procedure = returnData.items[z]['procedure']
                    var item = returnData.items[z]['item']
                    var description = returnData.items[z]['description'];
                    var units = returnData.items[z]['units'];
                    var value = returnData.items[z]['value_cent']
                    if(sub_category) {
                        if(sub_sub_category) {
                            if(sub_sub_sub_category) {
                                b.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul></li></ul>";
                            }
                            else {
                            b.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul>";
                            }
                        }
                        else {
                            b.innerHTML = category + "<ul><li>" + sub_category + "</li></ul>";
                        }
                    }
                    else {
                        b.innerHTML = category + "<br>";
                    }
                    if (procedure){
                        b.innerHTML += "<p style='font-style: italic;'>" + procedure + "</p>";
                    }
                    wrapper_b.innerHTML += "<p style='margin:0;'id='items-list-item"+ z +"'><strong>" + items[z].substr(0, val.length) + "</strong>" + items[z].substr(val.length) + "</p>";
                    wrapper_b.innerHTML += "<p style='margin:0;'id='items-list-description"+ z +"'>&nbsp;" + description + "</p>";
                    wrapper_b.innerHTML += "<input type='hidden' id='items-list-input" + z + "'  value='" + item + "'>";
                    wrapper_b.innerHTML += "<input type='hidden' id='items-list-input-units" + z + "'  value='" + units + "'>";
                    wrapper_b.innerHTML += "<input type='hidden' id='items-list-input-value" + z + "'  value='" + value + "'>";
                    b.appendChild(wrapper_b);
                    (function(index){
                        b.addEventListener("click", function() {
                            var value_of_value = document.getElementById("value-0").value
                            if(value_of_value){
                                clone()
                            }    
                            next_empty_treatment_input = document.getElementById("tbodyClone").lastElementChild.childNodes[3].firstChild
                          
                            item_num = document.getElementById("items-list-input" + index).value;
                            next_empty_treatment_input.value = item_num;

                            description_text = document.getElementById("items-list-description" + index).textContent;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].value = description_text;

                            units = document.getElementById("items-list-input-units" + index).value;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].value = units / 100;

                            value = document.getElementById("items-list-input-value" + index).value;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].value = value / 100;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[11].childNodes[0].value = value / 100;

                            closeAllLists();
                        })
                    })(z)
                    a.appendChild(b);
                }
            }


            procedures_length = returnData.procedures.length;
            if(procedures_length > 0){
                var middle_div = document.createElement("DIV");
                var treatments_from_procedures = [], range = procedures_length;
                var procedures_from_procedures = [], range = procedures_length;
                var arr_unique = [];
                for(i = 0; i < procedures_length; i++){
                    procedures_from_procedures[i] = returnData.procedures[i]['procedure'];
                    arr_unique = uniq_fast(procedures_from_procedures);
                }
                var found = [], range = arr_unique.length;
                for(i = 0; i < arr_unique.length; i++){
                    found[i] = returnData.procedures.filter(function(single) {
                        return single.procedure == arr_unique[i];})
                    }
                let index_treatment_procedure = 0;
                for (i = 0; i < arr_unique.length; i++){
                    var y = document.createElement("DIV");
                    y.style.cursor = "default";
                    var category = returnData.procedures[i]['category'];
                    var sub_category = returnData.procedures[i]['sub_category'];
                    var sub_sub_category = returnData.procedures[i]['sub_sub_category']
                    var sub_sub_sub_category = returnData.procedures[i]['sub_sub_sub_category']
                    var procedure = returnData.procedures[i]['procedure']
                    var item = returnData.procedures[i]['item']
                    if(sub_category) {
                        if(sub_sub_category) {
                            if(sub_sub_sub_category) {
                                y.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul></li></ul>";
                            }
                            else {
                            y.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul>";
                            }
                        }
                        else {
                            y.innerHTML = category + "<ul><li>" + sub_category + "</li></ul>";
                        }
                    }
                    else {
                        y.innerHTML = category + "<br>";
                    }

                    y.innerHTML += "<strong>" + arr_unique[i].substr(0, val.length) + "</strong>";
                    y.innerHTML += arr_unique[i].substr(val.length) + "<br>";

                    for(x=0; x < found[i].length; x++){
                        index_treatment_procedure++;

                        var flex_wrapper = document.createElement("DIV");
                        flex_wrapper.style.display = "flex";
                        flex_wrapper.style.justifyContent = "flex-start";
                        flex_wrapper.style.alignItems = "center";
                        
                        
                        var paragraph_field = document.createElement("P");     
                        paragraph_field.setAttribute("id", "procedure-list-description" + index_treatment_procedure)
                        paragraph_field.style.margin = "0";      
                        paragraph_field.textContent = found[i][x]['description']
                        paragraph_field.setAttribute('class','input-fields-procedures')
                        flex_wrapper.appendChild(paragraph_field)

                        var input_field = document.createElement("INPUT");
                        input_field.setAttribute("id", "treatment-list-input-procedure" + index_treatment_procedure)
                        input_field.readOnly = true;
                        input_field.style.cursor = "default";
                        input_field.style.border =  "none";
                        input_field.style.backgroundColor = 'white';
                        input_field.value = found[i][x]['item']
                        flex_wrapper.appendChild(input_field)

                        var value_input_field = document.createElement("INPUT");
                        value_input_field.setAttribute("id", "treatment-list-value-input-procedure" + index_treatment_procedure)
                        value_input_field.style.display = "none";
                        value_input_field.value = found[i][x]['value_cent'];
                        flex_wrapper.appendChild(value_input_field);

                        var units_input_field = document.createElement("INPUT");
                        units_input_field.setAttribute("id", "treatment-list-units-input-procedure" + index_treatment_procedure)
                        units_input_field.style.display = "none";
                        units_input_field.value = found[i][x]['units'];
                        flex_wrapper.appendChild(units_input_field);

                        (function(index){
                                paragraph_field.addEventListener("click", function() {

                                    //TODO this needs a better solution
                                    var value_of_value = document.getElementById("value-0").value
                                    if(value_of_value){
                                        clone()
                                    } 

                                    next_empty_treatment_input = document.getElementById("tbodyClone").lastElementChild.childNodes[3].firstChild

                                    item_num = document.getElementById("treatment-list-input-procedure" + index).value
                                    next_empty_treatment_input.value = item_num

                                    description_procedures = document.getElementById("procedure-list-description" + index).textContent;
                                    next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].value = description_procedures

                                    units_procedures = document.getElementById("treatment-list-units-input-procedure" + index).value;
                                    next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].value = units_procedures / 100

                                    value_procedures = document.getElementById("treatment-list-value-input-procedure" + index).value;
                                    next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].value = value_procedures / 100
                                    next_empty_treatment_input.parentNode.parentNode.childNodes[11].childNodes[0].value = value_procedures / 100

                                    next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].style.display = "block";
                                    next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].style.display = "block";
                                    next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].style.display = "block";

                                    closeAllLists();
                                })
                            })(index_treatment_procedure)     
                            y.appendChild(flex_wrapper)       
                    }
                    middle_div.appendChild(y);
                }
                a.appendChild(middle_div);    
            }

            for (i = 0; i < names.length; i++) {
                if (names[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                    var b = document.createElement("DIV");
                    var wrapper_b = document.createElement("DIV");
                    b.setAttribute('class','treatment-divs')
                    wrapper_b.style.display = "flex";
                    wrapper_b.style.justifyContent = "flex-start";
                    wrapper_b.style.alignItems = "center";
                    var category = returnData.treatments[i]['category'];
                    var sub_category = returnData.treatments[i]['sub_category'];
                    var sub_sub_category = returnData.treatments[i]['sub_sub_category']
                    var sub_sub_sub_category = returnData.treatments[i]['sub_sub_sub_category']
                    var procedure = returnData.treatments[i]['procedure']
                    var item = returnData.treatments[i]['item']
                    var value_cent = returnData.treatments[i]['value_cent']
                    var units = returnData.treatments[i]['units']
                    if(sub_category) {
                        if(sub_sub_category) {
                            if(sub_sub_sub_category) {
                                b.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul></li></ul>";
                            }
                            else {
                            b.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul>";
                            }
                        }
                        else {
                            b.innerHTML = category + "<ul><li>" + sub_category + "</li></ul>";
                        }
                    }
                    else {
                        b.innerHTML = category + "<br>";
                    }
                    if (procedure){
                        b.innerHTML += "<p style='font-style: italic;'>" + procedure + "</p>";
                    }
                    wrapper_b.innerHTML += "<p style='margin:0;'id='treatment-list-description"+ i +"'><strong>" + names[i].substr(0, val.length) + "</strong>" + names[i].substr(val.length) + "</p>";
                    wrapper_b.innerHTML += "<input style='background-color:white; cursor:pointer;'id='treatment-list-input" + i + "'  value='" + item + "'>";
                    wrapper_b.innerHTML += "<input style='display: none' id='treatment-list-value-input" + i + "'  value='" + value_cent + "'>";
                    wrapper_b.innerHTML += "<input style='display: none' id='treatment-list-units-input" + i + "'  value='" + units + "'>";
                    b.appendChild(wrapper_b);

                    (function(index){
                        b.addEventListener("click", function() {
                            var value_of_value = document.getElementById("value-0").value
                            if(value_of_value){
                                clone()
                            }      
                            next_empty_treatment_input = document.getElementById("tbodyClone").lastElementChild.childNodes[3].firstChild

                            description_text = document.getElementById("treatment-list-description"+ index).textContent;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].value = description_text

                            item_num = document.getElementById("treatment-list-input" + index).value
                            next_empty_treatment_input.value = item_num


                            var units_procedures = document.getElementById("treatment-list-units-input"+ index).value;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].value = units_procedures / 100

                            value_cent = document.getElementById("treatment-list-value-input" + index).value;
                            next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].value = value_cent / 100
                            next_empty_treatment_input.parentNode.parentNode.childNodes[11].childNodes[0].value = value_cent / 100
                            
                            next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].style.display = "block";
                            next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].style.display = "block";
                            next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].style.display = "block";
                            

                            closeAllLists();
                        })
                    })(i)
                    a.appendChild(b);
                }
            }

            var categories_length = returnData.categories.length;
            if(categories_length > 0){
                var categories_div = document.createElement("DIV");
                var treatments_from_category = [], range = categories_length;
                var category_from_categories = [], range = categories_length;
                var category_unique = [];
                for(i = 0; i < categories_length; i++){
                    category_from_categories[i] = returnData.categories[i]['category']
                    category_unique = uniq_fast(category_from_categories)
                }
                var found_items_from_category = [], range = category_unique.length;
                if(category_unique){
                    for(i = 0; i < category_unique.length; i++){
                        found_items_from_category[i] = returnData.categories.filter(function(single) {
                        return single.category == category_unique[i];})

                        var category_div = document.createElement("DIV");
                        var category = returnData.categories[i]['category'];
                        var sub_category = returnData.categories[i]['sub_category'];
                        var sub_sub_category = returnData.categories[i]['sub_sub_category']
                        var sub_sub_sub_category = returnData.categories[i]['sub_sub_sub_category']
                        var procedure = returnData.categories[i]['procedure']
                        var item = returnData.categories[i]['item']
                        if(sub_category) {
                            if(sub_sub_category) {
                                if(sub_sub_sub_category) {
                                    category_div.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul></li></ul>";
                                }
                                else {
                                    category_div.innerHTML = category + "<ul><li>" + sub_category + "<ul><li>" + sub_sub_category + "</li></ul></li></ul>";
                                }
                            }
                            else {
                                category_div.innerHTML = category + "<ul><li>" + sub_category + "</li></ul>";
                            }
                        }
                        else {
                            category_div.innerHTML = category + "<br>";
                        }
                        for(x=0; x < found_items_from_category[i].length; x++){
                            var flex_wrapper = document.createElement("DIV");
                            flex_wrapper.style.display = "flex";
                            flex_wrapper.style.justifyContent = "flex-start";
                            flex_wrapper.style.alignItems = "center";
                            category_div.appendChild(flex_wrapper);
                            
                            var paragraph_field = document.createElement("P"); 
                            paragraph_field.setAttribute("id", "category-list-description" + x)
                            paragraph_field.style.margin = "0";
                            paragraph_field.style.cursor = "pointer";
                            paragraph_field.textContent = found_items_from_category[i][x]['description'];
                            paragraph_field.setAttribute('class','input-fields-category');
                            flex_wrapper.appendChild(paragraph_field);

                            var input_field = document.createElement("INPUT");
                            input_field.setAttribute("id", "category-list-input-items" + x)
                            input_field.readOnly = true;
                            input_field.style.cursor = "default";  
                            input_field.style.backgroundColor = 'white';
                            input_field.value = found_items_from_category[i][x]['item'];
                            flex_wrapper.appendChild(input_field);

                            var value_input_field = document.createElement("INPUT");
                            value_input_field.setAttribute("id", "category-list-input-value" + x)
                            value_input_field.setAttribute("type", "hidden")
                            value_input_field.value = found_items_from_category[i][x]['value_cent'];
                            flex_wrapper.appendChild(value_input_field);


                            var units_input_field = document.createElement("INPUT");
                            units_input_field.setAttribute("id", "category-list-input-units" + x)
                            units_input_field.setAttribute("type", "hidden")
                            units_input_field.value = found_items_from_category[i][x]['units'];
                            flex_wrapper.appendChild(units_input_field);
                            
                            (function(index){
                                    paragraph_field.addEventListener("click", function() {
                                        var value_of_value = document.getElementById("value-0").value
                                        if(value_of_value){
                                            clone()
                                        } 
                                        next_empty_treatment_input = document.getElementById("tbodyClone").lastElementChild.childNodes[3].firstChild

                                        item_num = document.getElementById("category-list-input-items" + index).value
                                        next_empty_treatment_input.value = item_num

                                        description_categories = document.getElementById("category-list-description" + index).textContent;
                                        next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].value = description_categories

                                        var units_item = document.getElementById("category-list-input-units" + index).value;
                                        next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].value = units_item / 100

                                        var value_item = document.getElementById("category-list-input-value" + index).value;
                                        next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].value = value_item / 100
                                        next_empty_treatment_input.parentNode.parentNode.childNodes[11].childNodes[0].value = value_item / 100

                                        
                                        

                                        next_empty_treatment_input.parentNode.parentNode.childNodes[5].childNodes[0].style.display = "block";
                                        next_empty_treatment_input.parentNode.parentNode.childNodes[7].childNodes[0].style.display = "block";
                                        next_empty_treatment_input.parentNode.parentNode.childNodes[9].childNodes[0].style.display = "block";
                                        closeAllLists();
                                    })
                                })(x);     
                        }
                        categories_div.appendChild(category_div);
                    }
                }
                a.appendChild(categories_div);
            }
            function closeAllLists(elmnt) {
                var x = document.getElementsByClassName("autocomplete-items2");
                for (var i = 0; i < x.length; i++) {
                    if (elmnt != x[i] && elmnt != input_element) {
                    x[i].parentNode.removeChild(x[i]);
                    }
                }     
            }
            document.addEventListener("click", function (e) {
                closeAllLists(e.target);
                $('#treatmentsearch').val('');
            })
        }
    })

}