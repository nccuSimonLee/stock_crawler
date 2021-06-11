from datetime import datetime, timedelta



def ptt_time_to_dt(time_str):
    time_str = time_str.split('/')[0]
    dt = datetime.strptime(time_str, '%a %b %d %H:%M:%S %Y')
    return dt

def cmoney_time_to_dt(time_str):
    return datetime.strptime(time_str, '%Y/%m/%d %H:%M')

def adjust_dt(raw_dt):
    backoff_start, backoff_end = get_backoff_span(raw_dt)
    if backoff_start <= raw_dt < backoff_end:
        dt = raw_dt - timedelta(days=1)
    else:
        dt = raw_dt
    return dt

def get_backoff_span(dt):
    backoff_start = datetime(
        dt.year,
        dt.month,
        dt.day,
        0,
        0,
        0
    )
    backoff_end = datetime(
        dt.year,
        dt.month,
        dt.day,
        13,
        30,
        0
    )
    return (backoff_start, backoff_end)