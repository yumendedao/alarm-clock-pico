from machine import Pin, I2C
from clock import alarm_clock

i2c=I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)
# i2c=I2C(1, scl=Pin(19),sda=Pin(18), freq=100000)

from ssd1306 import SSD1306_I2C
oled = SSD1306_I2C(128, 32, i2c)


show_time_flag = True;

def clear_screen():
    oled.fill(0)
    oled.show()


def show_time():
    time_str = alarm_clock.get_time_show_str()
    alarm_time_str = alarm_clock.get_alarm_show_str()
    clear_screen()
    oled.text(time_str, 0, 6)
    oled.text(alarm_time_str, 0, 18)
    oled.show()
    return time_str




