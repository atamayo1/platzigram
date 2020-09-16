# Django
from django.http import HttpResponse

# Utilities
from datetime import datetime
import json

def hello_world(request):
    return HttpResponse('Oh, hi! Current server time is {now}'.format(
        now = datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
    ))

def sorted_integers(request):
   # Debugger: import pdb; pdb.set_trace()
    numbers = request.GET['numbers']
    data = {
        'status': 'ok',
        'numbers': sorted(numbers.split(',')),
        'message': 'Integers sorted successfully'
    }
    return HttpResponse(json.dumps(data, indent=4), content_type='application/json')

def say_hi(request, name, age):
    if age < 12:
        message =  'Sorry {}, you are not allowed here'.format(name)
    else:
        message = f'Hola, {name}! Welcome to Platzigram'
    return HttpResponse(message)