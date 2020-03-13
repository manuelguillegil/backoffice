
/* This code prevents the default submit from a form  modal for a new task.
    then, it sends a POST request with the current form data to store a
    new task without refresh
*/

var submissions = 0;

//If 
$(document).on('click', '.submitEdit', function(){
    console.log("I submit once");
});

$(document).on('submit', '.edit-task-mod-form',function(e){

    e.preventDefault();
    console.log(e.target.id);
    submissions += 1;
    console.log("Submiteo: " + submissions);
    
    //console.log($('#registerTaskMod').serialize());

    //console.log(dataUrl);

    /**
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
    */
});


