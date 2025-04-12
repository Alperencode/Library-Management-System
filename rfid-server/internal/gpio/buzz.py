from gpiozero import Buzzer, LED
from time import sleep

buzzer = Buzzer(18)
led = LED(23)


def buzz(duration=0.1):
    buzzer.on()
    led.on()
    sleep(duration)
    buzzer.off()
    led.off()
