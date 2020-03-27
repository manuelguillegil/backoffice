def clock_variable(request):
    if request.user.is_authenticated:
        clock = '--:--:--'

        clock_var = request.user.userprofile
    
        clock_last_task = clock_var.clock_last_task
        request.user.userprofile.save()
        request.user.save()

        clock_last_init = clock_var.clock_last_init
        request.user.userprofile.save()
        request.user.save()

        clock_status = clock_var.clock_status
        if(clock_status==None or clock_status<0 or clock_status>2):
            clock_status = 0
        clock_var.clock_status = clock_status
        request.user.userprofile.save()
        request.user.save()

         #clock = clock_var.clock
        if(clock_status != 1):
            clock = clock_var.clock
        #    clock = '00:00:00'
        #clock_var.clock = clock
        #request.user.userprofile.save()
        #request.user.save()
        
        return {
            'clock': clock,
            'clock_status' : clock_status,
            'clock_last_task' : clock_last_task,
            'clock_last_init' : clock_last_init,
        }