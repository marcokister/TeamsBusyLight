import pyautogui
import time
from datetime import datetime
import serial
import configparser

# region ---- Konstanten Parameter Initialisierung----

config = configparser.ConfigParser()
config.read('config.ini')

PICO_PORT = config["USB"]["port"]
PIXEL_X = int(config["PIXEL"]["pixelx"])
PIXEL_Y = int(config["PIXEL"]["pixely"])
RED_RGB = tuple(map(int, config["PIXEL"]["pixelcolor"].split(",")))
TOLERANCE = int(config["PIXEL"]["pixeltolerance"])

#PICO_PORT = 'COM5'
ser = serial.Serial(PICO_PORT, 115200, timeout=1)

# endregion

# region ---- loeschen
# Erfasste Koordinaten des roten Punkts im Taskleisten-Icon
#PIXEL_X = 1721
#PIXEL_Y = 1059

# Reines Rot + Toleranzbereich
#RED_RGB = (196, 49, 75)
#TOLERANCE = 15

# endregion


def send_to_pico(state):
    try:
        if state == "busy":
            ser.write(b'ON\n')
        else:
            ser.write(b'OFF\n')
    except Exception as e:
        print(f"[USB-Fehler] {e}")


def is_red(pixel, reference, tolerance):
    return all(abs(pixel[i] - reference[i]) <= tolerance for i in range(3))


def is_teams_busy():
    pixel = pyautogui.pixel(PIXEL_X, PIXEL_Y)
    return is_red(pixel, RED_RGB, TOLERANCE)


def monitor_teams_status():
    print("📡 Starte Teams-Statusüberwachung über Taskleisten-Icon...")
    print(f"🔍 Überwache Pixel an Position ({PIXEL_X}, {PIXEL_Y})...")
    last_state = None
    while True:
        try:
            busy = is_teams_busy()
            if busy != last_state:
                timestamp = datetime.now().strftime("%H:%M:%S")
                status = "🔴 Teams: Besetzt" if busy else "🟢 Teams: Nicht besetzt"
                print(f"{timestamp} – {status}")

                send_to_pico("busy" if busy else "free")

                last_state = busy
            time.sleep(3)
        except KeyboardInterrupt:
            print("\n🛑 Überwachung manuell beendet.")
            break
        except Exception as e:
            print(f"[Fehler] {e}")
            time.sleep(5)


if __name__ == "__main__":
    monitor_teams_status()
