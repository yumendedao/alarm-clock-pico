#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import _thread

hour = 0
minute = 0
second = 0
time_start_flag = True

alarm_hour = 0
alarm_minute = 0

change_type_set = 0
change_type_add = 1
change_type_sub = 2


def get_hour():
    global hour
    if hour < 0 or hour >= 24:
        hour = 0
    return hour


def get_minute():
    global minute
    if minute < 0 or minute >= 60:
        minute = 0
    return minute


def get_second():
    global second
    if second < 0 or second >= 60:
        second = 0
    return second


def get_time_str(time_type=None):
    if 'hour' == time_type:
        time_value = get_hour()
    elif 'minute' == time_type:
        time_value = get_minute()
    elif 'second' == time_type:
        time_value = get_second()
    else:
        print('get_time_str error type: ' + str(time_type))
        return
    if time_value < 10:
        time_value = '0' + str(time_value)
    else:
        time_value = str(time_value)
    return time_value


def get_time_show_str():
    time_str = get_time_str('hour') + ':' + get_time_str('minute') + ':' + get_time_str('second')
    print('time_str=' + time_str)
    return time_str


def change_time(time_type=None, change_type=change_type_set, value=None):
    if not check_time_type(time_type):
        return
    if value is None or not value.isdigit():
        print('change_time error value:' + str(value))
        return

    if 'hour' == time_type:
        global hour
        if change_type == change_type_set:
            hour = value
        elif change_type == change_type_add:
            hour = hour + value
        elif change_type == change_type_sub:
            hour = hour - value
        get_hour()
    elif 'minute' == time_type:
        global minute
        if change_type == change_type_set:
            minute = value
        elif change_type == change_type_add:
            minute = hour + value
        elif change_type == change_type_sub:
            minute = hour - value
        get_minute()
    elif 'second' == time_type:
        global second
        if change_type == change_type_set:
            second = value
        elif change_type == change_type_add:
            second = hour + value
        elif change_type == change_type_sub:
            second = hour - value
        get_second()
    else:
        print('change_time error time_type: ' + str(time_type))
        return
    return


def check_time_type(time_type):
    if 'hour' == time_type or 'minute' == time_type or 'second' == time_type:
        return True
    else:
        print('error time_type: ' + str(time_type))
        return False


def is_alarm():
    return hour == alarm_hour and minute == alarm_minute


def start():
    global time_start_flag
    time_start_flag = True
    init()


def stop():
    global time_start_flag
    time_start_flag = False


def time_run():

    while True:
        time_str = get_time_show_str()
        print(time_str)
        global time_start_flag
        if not time_start_flag:
            print('time stop, time_str=' + str(time_str))
            return
        time.sleep(1)
        global second, minute, hour
        second = second + 1
        if second >= 60:
            second = 0
            minute = minute + 1
        if minute >= 60:
            minute = 0
            hour = hour + 1
        if hour >= 24:
            hour = 0
    return


def init():
    _thread.start_new_thread(time_run, [])

