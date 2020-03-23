$(document).ready(function(){

    var timerId = 0; //timeInterval object id
    var timePassed = 0; //Time passed
    var timeToDelete = 1000; //total time to pass
    $deleteBtn = $('.delete-btn');



   $deleteBtn.on('mousedown touchstart',function(e){
        
        console.log($(e.target)[0].id);
        showBar();
        //timerId = setInterval(timeHandler,timeInterval);
        
    }).bind('mouseup', function() {
        hideBar()
        //clearInterval(timerId);
        console.log("pasó: " + timePassed);
        timePassed = 0;
        });
    /*
    $deleteBtn.mousedown(function(e){
        if(state == states.waiting){
            console.log("hold on...");
            state = states.counting;
            showBar();
            timerId = setInterval(timeHandler,timeInterval);
        }
        return false;
    });
    */

    // Helper functions
    function timeHandler(){
        
    }

    function deleteTask(){
        alert("Tarea eliminada");
    }

    function showBar(){
        var $progressBar = $('#progress-bar');
        $progressBar.removeClass('invisible');
    }

    function hideBar(){
        var $progressBar = $('#progress-bar');
        $progressBar.addClass('invisible');
    }
});


