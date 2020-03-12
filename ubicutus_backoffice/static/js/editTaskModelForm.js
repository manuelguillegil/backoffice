
/* This code prevents the default submit from a form  modal for a new task.
    then, it sends a POST request with the current form data to store a
    new task without refresh
*/
$(document).ready(function(){
    console.log("Mi id es: " + formId);

});
$(document).on('submit', formId, function(e){

    console.log("no entiendo lo que está pasando");
    e.preventDefault();
    
    var formData = $(formId).serialize();

    
    $.ajax({
        type:'POST',
        url: dataUrl,
        
        data:  formData,
        success:function(json){
            console.log(json);
        },
        error : function(xhr,errmsg,err) {
            console.log("Error:");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
    
});
