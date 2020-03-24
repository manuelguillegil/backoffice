def clock_variable(request):
    clock = '00:00:00'
    
    if 'clock' not in request.session:
        request.session['clock'] = clock
        request.session.save()
    else:
        clock = request.session['clock']
    
    return {
        'clock': clock
    }