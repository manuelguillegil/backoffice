
/* This code prevents the default submit from a form  modal for a new task*/

$(document).ready(function(){
    console.log('{% url "registrar_tarea" %}');
});

$(document).on('submit', '#registerTaskMod',function(e){

    e.preventDefault();
    
    console.log($('#registerTaskMod').serialize());

    $.ajax({
        type:'POST',
        url:'http://127.0.0.1:8000/registrar_tareas/',
        /** 
        data:{
			name        : $('#taskName').val(),
			description : $('#taskDescript').val(),
			init_date   : $('#taskInitDate').val(),
			end_date    : $('#taskEndDate').val(),
			status      : $('#taskStatus').val(),
            user        : ["{{user.id}}"],
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
 
        },
        */
       data:  $('#registerTaskMod').serialize(),
        success:function(json){
            console.log(json);
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
});


