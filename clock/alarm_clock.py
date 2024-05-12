#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import _thread
from clock import clock_control

hour = 0
minute = 0
second = 0
second = 58
time_start_flag = True

alarm_hour = 0
alarm_minute = 1
alarm_flag = False

change_type_set = 0
change_type_add = 1
change_type_sub = 2
set_flash = False
flash_count = 0

set_close_index = 0
hour_index = 1
minute_index = 2
second_index = 3
alarm_hour_index = 4
alarm_minute_index = 5

clock_seq = [set_close_index, hour_index, minute_index, second_index, alarm_hour_index, alarm_minute_index]


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


def get_alarm_hour():
    global alarm_hour
    if alarm_hour < 0 or alarm_hour >= 24:
        alarm_hour = 0
    return alarm_hour


def get_alarm_minute():
    global alarm_minute
    if alarm_minute < 0 or alarm_minute >= 60:
        alarm_minute = 0
    return alarm_minute


def get_time_str(time_type=None):
    global flash_count

    if clock_control.set_index == time_type:
        flash_count = flash_count + 1
        print(flash_count)
        if flash_count > 2:
            flash_count = 0            
            return '  '

    if clock_control.set_index == set_close_index:
        flash_count = 0

    if hour_index == time_type:
        time_value = get_hour()
    elif minute_index == time_type:
        time_value = get_minute()
    elif second_index == time_type:
        time_value = get_second()
    elif alarm_hour_index == time_type:
        time_value = get_alarm_hour()
    elif alarm_minute_index == time_type:
        time_value = get_alarm_minute()
    else:
        print('get_time_str error type: ' + str(time_type))
        return
    if time_value < 10:
        time_value = '0' + str(time_value)
    else:
        time_value = str(time_value)

    return time_value


def get_time_show_str():
    time_str = get_time_str(hour_index) + ':' + get_time_str(minute_index) + ':' + get_time_str(second_index)
    return time_str


def get_alarm_show_str():
    return 'alarm  ' + get_time_str(alarm_hour_index) + ':' + get_time_str(alarm_minute_index) + ":00"


def change_time(time_type=None, change_type=change_type_set, value=None):
    print('change_time, time_type:' + str(time_type) + ", change_type:" + str(change_type) + ", value:" + str(value))
    if not check_time_type(time_type):
        return

    if hour_index == time_type:
        global hour
        if change_type == change_type_set:
            hour = value
        elif change_type == change_type_add:
            if hour==23:
                hour = 0
            else:
                hour = hour + value
        elif change_type == change_type_sub:
            if hour==0:
                hour = 23
            else:
                hour = hour - value
        get_hour()
    elif minute_index == time_type:
        global minute
        if change_type == change_type_set:
            minute = value
        elif change_type == change_type_add:
            if minute == 59:
                minute = 0
            else:
                minute = minute + value
        elif change_type == change_type_sub:
            if minute == 0:
                minute = 59
            else:
                minute = minute - value
        get_minute()
    elif second_index == time_type:
        global second
        if change_type == change_type_set:
            second = value
        elif change_type == change_type_add:
            if second == 59:
                second = 0
            else:
                second = second + value   
        elif change_type == change_type_sub:
            if second == 0:
                second = 59
            else:second = second - value
        get_second()
    elif alarm_hour_index == time_type:
        global alarm_hour
        if change_type == change_type_set:
            alarm_hour = value
        elif change_type == change_type_add:
            if alarm_hour==23:
                alarm_hour = 0
            else:
                alarm_hour = alarm_hour + value
        elif change_type == change_type_sub:
            if alarm_hour == 0:
                alarm_hour = 23
            else:
                alarm_hour = alarm_hour - value
        get_alarm_minute()
    elif alarm_minute_index == time_type:
        global alarm_minute
        if change_type == change_type_set:  
            alarm_minute = value
        elif change_type == change_type_add:
            if alarm_minute == 59:
                alarm_minute = 0
            else:
                alarm_minute = alarm_minute + value
        elif change_type == change_type_sub:
            if alarm_minute == 0:
                alarm_minute = 59
            else:
                alarm_minute = alarm_minute - value
        get_alarm_minute()
    else:
        print('change_time error time_type: ' + str(time_type))
        return
    return


def check_time_type(time_type):
    if time_type < 0 or time_type >= len(clock_seq):
        print('error time_type: ' + str(time_type))
        return False
    else:
        return True


def is_alarm():
    return hour == alarm_hour and minute == alarm_minute and second == 0


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
            print('time_start_flag false, time stop, time_str=' + str(time_str))
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




