function clone() {
    $(".clonedInput").last().clone()
        .appendTo(".tbodyClone")
        .attr("id", "clonedInput" + cloneIndex)
        .find("*")
        .each(function () { 
             var id = this.id || "";
             var match = id.match(regex) || [];  
             if (match.length == 4) {
                 this.id = match[1] + (cloneIndex);
             }
             if (this.className.includes("treatment")){
                this.value = ''
             } 
             if (this.className.includes("description")){
                this.value = ''
             } 
             if (this.className.includes("value")){
                this.value = ''
             } 
             if (this.className.includes("postvalue")){
                this.value = ''
             } 
             if (this.className.includes("date")){
                this.value = ''
             } 
             if (this.className.includes("row")){
                this.remove();
             } 
        })
    cloneIndex++;
    if ($(".clonedInput").length == 1) {
        $('.remove').hide();
    } else {
        $('.remove').show();
    }
        $('table').find('tr').each(function(i, v) {
            $(v).find('span.num').text(i);
           
        });

    $('.popover-dismiss').popover({
            trigger: 'focus'
    })
    $('[data-toggle="popover"]').popover();
    // $(document).scrollTop($(document).height());
}