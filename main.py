# Code für Raspberry Pi Pico

import machine
import sys
import time

# interne LED GPIO 25
led = machine.Pin(25, machine.Pin.OUT)

# GPIO15 Relais
relais = machine.Pin(15, machine.Pin.OUT)

# Initialzustand: aus
led.value(0)
relais.value(0)

for i in range(0,2):
    led.value(1)
    time.sleep(.08)
    led.value(0)
    time.sleep(.08)

#print("Bereit. Warte auf PC...")

while True:
    try:
        command = sys.stdin.readline().strip()
        if command == "ON":
            led.value(1)
            relais.value(1)
        elif command == "OFF":
            led.value(0)
            relais.value(0)
    except Exception as e:
        print("Fehler:", e)



