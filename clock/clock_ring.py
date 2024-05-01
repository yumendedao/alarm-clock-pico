import _thread

import utime
from machine import ADC
from machine import Pin, PWM

from clock import time_show

buzzer = PWM(Pin(15))
buzzer.freq(262)
buzzer.duty_u16(0)

light = ADC(28)

ring_flag = False

L = [0, 262, 294, 330, 370, 410, 440, 494]
M = [0, 524, 588, 660, 740, 820, 880, 988]
H = [0, 1048, 1176, 1320, 1480, 1640, 1760, 1976]
Z = [0]


def get_value():
    return int(light.read_u16() * 101 / 65536)


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
    ring_flag = False


def task_to_be_triggered():
    ring_flag = True
    j = 0
    lightInit = get_value()
    print("lightInit:" + str(lightInit))
    alltime = 0
    song = choose_song(1)
    while j < 1:
        if not ring_flag:
            return
        j = j + 1
        k = 0
        for k in range(len(song) / 2):
            time_show.show_time()
            if not ring_flag:
                return
            pwm_tone(song[2 * k], song[2 * k + 1] * 5)
            alltime = alltime + song[2 * k + 1]
            if ((get_value() - lightInit) > 40 or (lightInit - get_value()) > 40 or alltime >= 3000):
                break
        if ((get_value() - lightInit) > 40 or (lightInit - get_value()) > 40 or alltime >= 3000):
            break


def ring():
    _thread.start_new_thread(task_to_be_triggered, [])
