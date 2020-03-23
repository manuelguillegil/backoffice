/* This code prevents the default submit from a form  modal for a new task.
    then, it sends a POST request with the current form data to store a
    new task without refresh
*/
$(document).on('submit', '#registerTaskMod',function(e){
    var $sendTask = $('#sendTask');
    var $errMsg  = $('#alert-add-error');
    var $succMsg = $('#alert-add-success');
    var $warMsg  = $('#alert-add-warning');

    e.preventDefault();
    $sendTask.attr('disabled', true);
    clearMsgs();

    ////////////Crear arreglo de datos para verificar y agregar action
    //convierte el form en arreglo de pares nombre-valor
    var data_arr = $('#registerTaskMod').serializeArray();
    var form_data = {};

    //load the form_data object with the form data
    data_arr.forEach(function(it,i){
        form_data[it.name] = it.value;
    });
    //sanity check
    console.log(form_data);
    ///////////////////

    //Check the fields:
    if(form_data.name==="" || form_data.description===""){
        raiseWarn();
        $sendTask.attr('disabled', false);
        return false;
    }
    //Send ajax if everything is ok
    $.ajax({
        type:'POST',
        url: dataUrl,
        
        data:  form_data,
        //data:  $('#registerTaskMod').serialize(),
        success:function(json){
            if(json.status == 'success'){
                raiseSucc();
            }
            else if(json.status == 'error'){
                raiseErr();
            }
            else{
                console.log('Undefined response received');
            }
        },
        error : function(xhr,errmsg,err) {
            //console.log(xhr.status + ": " + xhr.responseText);
            console.log(errmsg);
            raiseErr();
            $sendTask.attr('disabled', false);
        },
        dataType:'json'
    });
});


$(document).ready(function(){
    var $addBtn = $('#add-task-btn');

    //Clear the form when invoked
    $addBtn.click(function(e){
        cleanForm();
    });
    

});

//This functions clears all fields in the form and set the initial values
//of the date fields
function cleanForm(){
    var $myForm = $('#registerTaskMod');
    
    //Clear current values
    $myForm[0].reset();

    //Set init and end default values as today:
    document.getElementById('taskInitDate').valueAsDate = new Date();
    document.getElementById('taskEndDate').valueAsDate = new Date();

    //Just in case, reset the msgs
    clearMsgs();
}
//Clear every help msg
function clearMsgs(){
    var $errMsg  = $('#alert-add-error');
    var $succMsg = $('#alert-add-success');
    var $warMsg  = $('#alert-add-warning');

    $errMsg.addClass("d-none");
    $succMsg.addClass("d-none");
    $warMsg.addClass("d-none");
}

function raiseSucc(){
    $('#alert-add-success').removeClass("d-none");
}
function raiseWarn(){
    $('#alert-add-warning').removeClass("d-none");
}
function raiseErr(){
    $('#alert-add-error').removeClass("d-none");
}