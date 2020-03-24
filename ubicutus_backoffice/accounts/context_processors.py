from django.contrib.sessions.backends.db import SessionStore

def clock_current_state_to_context(request):
	
	# return None if there's not a current_task entry
	current_task = request.session.get('current_task')
	request.session['current_task'] = current_task 

	last_init_time = request.session.get('last_init_time')
	request.session['last_init_time'] = last_init_time 

	counter_hours1 = request.session.get('counter_hours1', 0)
	request.session['counter_hours1'] = counter_hours1 

	counter_hours2 = request.session.get('counter_hours2', 0)
	request.session['counter_hours2'] = counter_hours2 

	counter_mins1 = request.session.get('counter_mins1', 0)
	request.session['counter_mins1'] = counter_mins1 

	counter_mins2 = request.session.get('counter_mins2', 0)
	request.session['counter_mins2'] = counter_mins2 

	counter_sec1 = request.session.get('counter_sec1', 0)
	request.session['counter_sec1'] = counter_sec1 

	counter_sec2 = request.session.get('counter_sec2', 0)
	request.session['counter_sec2'] = counter_sec2 

	status = request.session.get('status', 'WAITING')
	request.session['status'] = status

	ret = {
		'current_task' : current_task,
		'last_init_time' : last_init_time,
		'counter_hours1' : counter_hours1,
		'counter_hours2' : counter_hours2,
		'counter_mins1' : counter_mins1,
		'counter_mins2' : counter_mins2,
		'counter_sec1' : counter_sec1,
		'counter_sec2' : counter_sec2,
		'status' : status,
	}

	return ret


""" 
https://stackoverflow.com/questions/2893724/creating-my-own-context-processor-in-django
https://dev.to/harveyhalwin/using-context-processor-in-django-to-create-dynamic-footer-45k4
https://docs.djangoproject.com/en/3.0/ref/templates/api/

__getitem__(key)

    Example: fav_color = request.session['fav_color']

__setitem__(key, value)

    Example: request.session['fav_color'] = 'blue'

__delitem__(key)

    Example: del request.session['fav_color']. This raises KeyError if the given key isn’t already in the session.

__contains__(key)

    Example: 'fav_color' in request.session

get(key, default=None)

    Example: fav_color = request.session.get('fav_color', 'red')

pop(key, default=__not_given)

    Example: fav_color = request.session.pop('fav_color', 'blue')
 """