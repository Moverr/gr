import time
import datetime

def format_date(date_str):
    time_tuple = time.strptime(date_str, "%Y-%m-%d")
    formatted_date = time.strftime("%d %B, %Y", time_tuple)
    return formatted_date

def get_time_ago(created_on):
    dt = datetime.datetime.strptime(created_on, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    diff = now - dt

    if diff.days > 7:
        return dt.strftime('%b %d, %Y')
    elif diff.days > 0:
        return f'{diff.days} days ago'
    elif diff.seconds > 3600:
        return f'{diff.seconds // 3600} hours ago'
    elif diff.seconds > 60:
        return f'{diff.seconds // 60} minutes ago'
    else:
        return 'just now'
