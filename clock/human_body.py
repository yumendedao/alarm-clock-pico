from machine import Pin

human = Pin(11, Pin.IN)
led = Pin(25, Pin.OUT)

abc = 0


# 打开主板自带的LED灯
def led_on():
    led.value(1)


# 关闭主板自带的LED灯
def led_off():
    led.value(0)


def detect_someone():
    if human.value() == 1:
        return True
    return False

