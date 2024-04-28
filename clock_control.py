import threading
import time

import alarm_clock
import time_show


def init():
    alarm_clock.start();
    clock_show()


def clock_show():
    time_show_thread = threading.Thread(target=clock_show_run)
    time_show_thread.start()


def clock_show_run():
    time_show_str = alarm_clock.get_time_show_str()
    while True:
        time_show.show_time(time_show_str)
        time.sleep(1)
