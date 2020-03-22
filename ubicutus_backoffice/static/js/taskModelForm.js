
/* This code prevents the default submit from a form  modal for a new task.
    then, it sends a POST request with the current form data to store a
    new task without refresh
*/
$(document).on('submit', '#registerTaskMod',function(e){

    e.preventDefault();
    
    console.log($('#registerTaskMod').serialize());

    console.log(dataUrl);

    $.ajax({
        type:'POST',
        url: dataUrl,
        
        data:  $('#registerTaskMod').serialize(),
        success:function(json){
            console.log(json);
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});


$(document).ready(function(){

});