
var currentStatus = null;



$(document).ready(function(){
    
    var select = $('#task-select');

    //The task description starts hidden

    select.change(function(e){
        var options = e.target.options;
        var currentOpt = options[options.selectedIndex];
        var noTaskMsg = $('#noTask');
        var taskInfo = $('#taskSelected');

        //if selected task is no-task
        if(currentOpt.value == '-1'){
            // If selected task is no-task, hide the task info section and show 
            // a no-task msg
            noTaskMsg.show();
            taskInfo.addClass("d-none");
        }
        else{
            // Otherwise, show the task info and hide the no-task msg
            noTaskMsg.hide();
            taskInfo.removeClass("d-none");

            //Update task information:
            updateTaskInfo(currentOpt);
        }


        console.log(currentOpt.value=='-1');
    });
    
});

//Given the selected option, updates the task information section
function updateTaskInfo(opt){
    var title = $('#task-title');
    var description = $('#task-description');
    var initDate = $('#task-init-date');
    var endDate = $('#task-end-date');
    var status = $('#task-status');
    var currentOpt = $("#" + opt.id);

    var statusBadges = {
        'New' : $('#status-new'),
        'In progress' : $('#status-in-prog'),
        'Waiting' : $('#status-freeze'),
        'Closed' : $('#status-done')
    };

    //Set the task data
    title.text(currentOpt.data("tname"));
    description.text(currentOpt.data("tdescrp"));
    initDate.text( currentOpt.data("indate") );
    endDate.text( currentOpt.data("endate") );

    //Set the current status
    if(currentStatus != null){
        currentStatus.addClass("d-none");
    }

    statusBadges[currentOpt.data("status")].removeClass("d-none");
    currentStatus = statusBadges[currentOpt.data("status")];
}