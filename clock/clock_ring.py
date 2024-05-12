import _thread
import random

import utime
import ws2812b
from machine import Pin, PWM
from ultrasonic import ultrasonic

from clock import time_show, human_body

Echo = Pin(13, Pin.IN)

Trig = Pin(14, Pin.OUT)

ultrasonic = ultrasonic(Trig, Echo)

# 蜂鸣器控件
buzzer = PWM(Pin(15))
buzzer.freq(262)
buzzer.duty_u16(0)

# light = ADC(28)

ring_pin = 17  # 灯环的引脚
numpix = 8  # RGB灯的数量
# 初始化RGB灯环
strip = ws2812b.ws2812b(numpix, 0, ring_pin)
strip.fill(0, 0, 0)  # 清空RGB缓存

ring_flag = False

L = [0, 262, 294, 330, 370, 410, 440, 494]
M = [0, 524, 588, 660, 740, 820, 880, 988]
H = [0, 1048, 1176, 1320, 1480, 1640, 1760, 1976]
Z = [0]


def get_value():
    return ultrasonic.Distance_accurate()


#     return int(light.read_u16() * 101 / 65536)


def choose_song(index):
    if index == 1:
        gyz = [M[6], 50, M[7], 50, H[1], 50, H[2], 50, M[7], 50, H[1], 50, H[1], 100, Z[0], 10,
               H[1], 50, M[7], 50, H[1], 50, H[2], 50, M[7], 50, H[1], 50, H[1], 100, Z[0], 10,
               H[1], 50, H[2], 50, H[3], 50, H[2], 50, H[3], 50, H[2], 50, H[3], 100, H[3], 50, H[3], 50, H[2], 50,
               H[3], 100, H[5], 100, H[3], 100, Z[0], 10
               ]
        return gyz
    return gyz


def pwm_tone(tone, time):
    if tone == 0:
        buzzer.duty_u16(0)
        utime.sleep_ms(time)
    else:
        buzzer.freq(tone)
        buzzer.duty_u16(32768)
        utime.sleep_ms(time)
        buzzer.duty_u16(0)


def close_ring():
    global ring_flag
    ring_flag = False
    strip.fill(0, 0, 0)
    strip.show()


def task_to_be_triggered():
    global ring_flag
    ring_flag = True
    j = 0
    lightInit = get_value()
    print("lightInit:" + str(lightInit))
    alltime = 0
    song = choose_song(1)
    while j < 3:
        if not ring_flag:
            return
        j = j + 1
        k = 0
        for k in range(len(song) / 2):
            time_show.show_time()
            ring_rgb()
            if human_body.detect_someone():
                human_body.led_on()
            else:
                human_body.led_off()
            if not ring_flag:
                return
            pwm_tone(song[2 * k], song[2 * k + 1] * 1)
            alltime = alltime + song[2 * k + 1]
            if ((get_value() - lightInit) > 40 or (lightInit - get_value()) > 40 or alltime >= 3000):
                break
        if ((get_value() - lightInit) > 40 or (lightInit - get_value()) > 40 or alltime >= 3000):
            break
    close_ring()


def ring():
    _thread.start_new_thread(task_to_be_triggered, [])


def ring_rgb():
    i = random.randint(0, numpix - 1)
    strip.show()
    strip.fill(0, 0, 0)
    r = random.randint(0, 256)
    g = random.randint(0, 256)
    b = random.randint(0, 256)
    # 设置RGB灯环中某个灯的颜色
    strip.set_pixel(i, r, g, b)
    strip.show()
