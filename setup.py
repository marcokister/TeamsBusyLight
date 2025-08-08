import pyautogui
import serial.tools.list_ports
import configparser

# ---------- Schritt 1: COM-Port wählen ----------
ports = list(serial.tools.list_ports.comports())
print("\n🔌 Angeschlossene serielle Geräte:")

if len(ports) == 0:
    print("❌ Keine seriellen Geräte gefunden. Abbruch.")
    exit(1)

for i, port in enumerate(ports):
    print(f"{i + 1}. {port.device} – {port.description}")

selected = input("➡️ Nummer des Ports wählen (z. B. 1): ")
try:
    port_index = int(selected) - 1
    selected_port = ports[port_index].device
except (ValueError, IndexError):
    print("❌ Ungültige Auswahl. Abbruch.")
    exit(1)



# ---------- Schritt 2: Pixelposition und Farbe erfassen ----------
input("\n🖱️ Bewege die Maus auf den roten Punkt im Teams-Icon und drücke ENTER...")
x, y = pyautogui.position()
color = pyautogui.pixel(x, y)
print(f"\n📍 Position: x={x}, y={y}")
print(f"🎨 Farbe an dieser Position: RGB = {color}")

# ---------- Schritt 3: Konfiguration speichern ----------
config = configparser.ConfigParser()

config["USB"] = {
    "port": selected_port
}

config["PIXEL"] = {
    "pixelx": str(x),
    "pixely": str(y),
    "pixelcolor": f"{color[0]}, {color[1]}, {color[2]}",
    "pixeltolerance": "15"
}

with open("config.ini", "w") as configfile:
    config.write(configfile)

print("\n✅ Konfiguration wurde erfolgreich in 'config.ini' gespeichert.")


"""import pyautogui
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

print("Angeschlossene serielle Geräte:")
for port in ports:
    print(f"• {port.device} – {port.description}")

input("Bewege die Maus auf den roten Punkt im Teams-Icon und drücke ENTER...")
x, y = pyautogui.position()
color = pyautogui.pixel(x, y)
print(f"Position erfasst: x={x}, y={y}")
print(f"Farbe an ({x}, {y}): RGB = {color}")
"""

