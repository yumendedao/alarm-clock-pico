import _thread

import utime
from machine import Pin, ADC

from clock import alarm_clock, time_show, clock_ring, human_body

# 初始化摇杆模块（ADC功能）: 遥感控件
rocker_x = ADC(27)
rocker_y = ADC(26)
button = Pin(22, Pin.IN, Pin.PULL_UP)

set_index = 0

set_value_up = 255
set_value_down = 0
btn_push = False
btn_release = True
set_change_once = False

human_body_flag = False
human_body_second = 0


# 读取X轴的值，返回[0, 255]
def read_x():
    value = int(rocker_x.read_u16() * 256 / 65536)
    return value


# 读取Y轴的值，返回[0, 255]
def read_y():
    value = int(rocker_y.read_u16() * 256 / 65536)
    return value


# 读取按键的状态，按下返回True，松开返回False
def btn_state():
    press = False
    if button.value() == 0:
        press = True
    return press


def init():
    alarm_clock.start()


def clock_show_run():
    global human_body_flag, human_body_second
    human_body_second = 0
    while True:
        time_show.show_time()
        set_change()
        if alarm_clock.is_alarm():
            clock_ring.task_to_be_triggered()

        if human_body.detect_someone():
            human_body_flag = True
            human_body_second = 0
            human_body.led_on()
        elif human_body_flag and human_body_second < 5:
            human_body_second = human_body_second + 1
            human_body.led_on()
        else:
            human_body_flag = False
            human_body_second = 0
            human_body.led_off()
        utime.sleep(0.5)


def clock_show():
    _thread.start_new_thread(clock_show_run, [])
    return


def clock_set_change():
    set_seq_length = len(alarm_clock.clock_seq)
    global set_index
    set_index = set_index + 1
    if set_index > set_seq_length:
        set_index = 0
    print('clock_set_change: ' + str(set_index))


#     return int(light.read_u16() * 101 / 65536)
def get_human_body_flag():
    if human_body.detect_someone():
        if human_body_flag:
            human_body_second = human_body_second + 1
        else:
            human_body_second = 0


def set_change():
    global set_index
    global btn_push, btn_release
    value_y = read_y()
    state = btn_state()
    if state:
        btn_push = True
    else:
        btn_release = True
    if btn_push and btn_release:
        clock_set_change()
        btn_push = False
        btn_release = True

    if set_index == alarm_clock.set_close_index:
        return
    elif value_y == set_value_up:
        print("set_value_up, set_index:" + str(set_index))
        if set_index == alarm_clock.hour_index:
            alarm_clock.change_time(alarm_clock.hour_index, alarm_clock.change_type_add, 1)
        elif set_index == alarm_clock.minute_index:
            alarm_clock.change_time(alarm_clock.minute_index, alarm_clock.change_type_add, 1)
        elif set_index == alarm_clock.second_index:
            alarm_clock.change_time(alarm_clock.second_index, alarm_clock.change_type_add, 1)
        elif set_index == alarm_clock.alarm_hour_index:
            alarm_clock.change_time(alarm_clock.alarm_hour_index, alarm_clock.change_type_add, 1)
        elif set_index == alarm_clock.alarm_minute_index:
            alarm_clock.change_time(alarm_clock.alarm_minute_index, alarm_clock.change_type_add, 1)
    elif value_y == set_value_down:
        print("set_value_down, set_index:" + str(set_index))
        if set_index == alarm_clock.hour_index:
            alarm_clock.change_time(alarm_clock.hour_index, alarm_clock.change_type_sub, 1)
        elif set_index == alarm_clock.minute_index:
            alarm_clock.change_time(alarm_clock.minute_index, alarm_clock.change_type_sub, 1)
        elif set_index == alarm_clock.second_index:
            alarm_clock.change_time(alarm_clock.second_index, alarm_clock.change_type_sub, 1)
        elif set_index == alarm_clock.alarm_hour_index:
            alarm_clock.change_time(alarm_clock.alarm_hour_index, alarm_clock.change_type_sub, 1)
        elif set_index == alarm_clock.alarm_minute_index:
            alarm_clock.change_time(alarm_clock.alarm_minute_index, alarm_clock.change_type_sub, 1)
