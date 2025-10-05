from datetime import datetime

def current_date(request):
    now = datetime.now()
    return {
        'date': now.date(),
        'year': now.year,
        'month': now.strftime('%B'),
        'time': now.strftime('%H:%M:%S')
    }

