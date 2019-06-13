import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('app.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def format_time(unix_timestamp):
    f = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(unix_timestamp)
    formatted = time.strftime(f, value)
    return formatted
