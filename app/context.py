import datetime

def get_user_context():
    context = {
        'time_of_day': datetime.datetime.now().hour,
        'day_of_week': datetime.datetime.now().weekday(),
        'mood': 'happy',
        'location': 'home',
        'energy_level': 'medium'
    }
    return context
