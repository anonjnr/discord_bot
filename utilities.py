import os
import time
import datetime
import threading
from calendar import timegm

TIME_ZONE = 'Europe/Berlin'

SECONDS_IN_A_MINUTE = 60
SECONDS_IN_AN_HOUR = SECONDS_IN_A_MINUTE * 60
SECONDS_IN_A_DAY = SECONDS_IN_AN_HOUR * 24
SECONDS_IN_A_WEEK = SECONDS_IN_A_DAY * 7


DAILY = 'daily'
WEEKLY = 'weekly'
DOY_YEAR_MILITARY = '%j%Y%H%M'
DAY_MILITARY = '%a:%H%M'
DOY_YEAR = '%j%Y'
DOY = '%j'
YEAR = '%Y'
MILITARY_TIME = '%H%M'
FMT_TIME = '%Y-%m-%d %H:%M'



# ALL TIME IS UTC

# EXAMPLE DECORATOR
def decorator(argument):

    def real_decorator(function):

        def wrapper(*args, **kwargs):
            print('1')
            print(argument)
            result = function(*args, **kwargs)
            print(2)
            return result
        return wrapper
    return real_decorator


def set_tz():
    os.environ['TZ'] = TIME_ZONE
    time.tzset()


# Wrapper
def log_time(do_print: bool=False):
    def real_log_time(orig_func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = orig_func(*args, **kwargs)
            time_lapsed = time.time() - start_time
            if do_print:
                print('{} completed {} seconds.'.format(orig_func.__name__.upper(), round(time_lapsed, 5)))

            return result
        return wrapper
    return real_log_time


def new_thread(funct: object) -> object:

    def wrapper(*args, **kwargs):
        print(funct.__name__.upper(), 'args:', args, 'kwargs:', kwargs)
        thr = threading.Thread(target=funct, args=args)
        thr.daemon = True
        return thr.start()

    return wrapper


def epoch(epoch=None, future_in_seconds: int=0, custom_hhmm: int=None):

    if epoch is None:  # if epoch is None return epoch now
        # epoch = int(datetime.datetime.now().strftime("%s"))
        epoch = int(time.time())

    if custom_hhmm is None:
        # return int(datetime.datetime.fromtimestamp(epoch + future_in_seconds).strftime("%s"))
        return int(time.time()) + future_in_seconds

    else:
        custom_timestamp = datetime.datetime.fromtimestamp(
            epoch + future_in_seconds).strftime(
            DOY_YEAR_MILITARY.replace('%H%M', str(custom_hhmm).zfill(4)))

        utc_time = time.strptime(custom_timestamp, DOY_YEAR_MILITARY)
        epoch_time = timegm(utc_time)

        return int(epoch_time)


def epoch_to_custom_date(fmt: str, _epoch: int=None):
    if _epoch is None:
        _epoch = epoch()
    return datetime.datetime.fromtimestamp(_epoch).strftime(fmt)


def get_week_number():
    now = datetime.datetime.now()
    return datetime.date(now.year, now.month, now.day).isocalendar()[1]

# set_tz()
