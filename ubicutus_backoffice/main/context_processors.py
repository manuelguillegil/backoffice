def clock_variable(request):
    clock = '00:00:00'

    clock = request.session.get('clock', clock)
    if(clock == ''):
        clock = '00:00:00'
    request.session['clock'] = clock
    request.session.save()

    clock_status = request.session.get('clock_status', 0)
    request.session['clock_status'] = clock_status
    request.session.save()

    clock_last_init = request.session.get('clock_last_init')
    if(clock_last_init!=None): request.session['clock_last_init'] = clock_last_init
    request.session.save()

    clock_task = request.session.get('clock_task')
    if(clock_task!=None): request.session['clock_task'] = clock_task
    request.session.save()
    
    return {
        'clock': clock,
        'clock_status' : clock_status,
    }