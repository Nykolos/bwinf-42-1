import sys
from PIL import Image

# Überprüfung auf richtige Eingabe
if len(sys.argv) != 2:
    print("Benutzung: main.py eingabe.png")
    sys.exit(0)

# Datei einlesen
img = Image.open(sys.argv[1]).convert("RGB")

# Größe des Bildes herausfinden
width, height = img.size

# Nachricht erstellen
msg = ""

# Startpunkt setzen
x = y = 0

# Abfrage
while True:

    # Pixel rgb Werte finden
    rgb = img.getpixel((x, y))

    # Rote Farbcode wird ASCII-Dekodiert
    msg += chr(rgb[0])

    # Die Grün und Blau werte werden bei x und y hinzugefügt
    x += rgb[1]
    y += rgb[2]

    # Überprüfung ob größer als Bildrand, dann abzug der Größe
    while x >= width:
        x -= width
    while y >= height:
        y -= height

    # Stop wenn die grün und blau Werte = 0 sind
    if rgb[1] == 0 and rgb[2] == 0:
        break

# Ausgabe der entschlüsselten Nachricht
print(msg)
