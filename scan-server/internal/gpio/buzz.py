from gpiozero import Buzzer, LED
from threading import Thread
from time import sleep

buzzer = Buzzer(18)

red_led = LED(22)
green_led = LED(27)
blue_led = LED(17)


def rgb_on(r=False, g=False, b=False):
    red_led.on() if r else red_led.off()
    green_led.on() if g else green_led.off()
    blue_led.on() if b else blue_led.off()


def buzz_and_blink(r=False, g=False, b=False, buzz_times=1, blink_times=1, duration=0.1):
    def _buzz():
        for _ in range(buzz_times):
            buzzer.on()
            sleep(duration)
            buzzer.off()
            sleep(duration)

    def _blink():
        for _ in range(blink_times):
            rgb_on(r, g, b)
            sleep(duration)
            rgb_on(False, False, False)
            sleep(duration)

    buzz_thread = Thread(target=_buzz)
    blink_thread = Thread(target=_blink)

    buzz_thread.start()
    blink_thread.start()

    buzz_thread.join()
    blink_thread.join()
