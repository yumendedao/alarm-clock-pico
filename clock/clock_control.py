import _thread
import utime

from clock import alarm_clock, time_show, clock_ring


def init():
    alarm_clock.start();


def clock_show_run():

    while True:
        time_show_str = alarm_clock.get_time_show_str()
        time_show.show_time(time_show_str)
        if alarm_clock.is_alarm():
            clock_ring.task_to_be_triggered()
        utime.sleep(1)
        
        


def clock_show():
    _thread.start_new_thread(clock_show_run, [])
    return



    
