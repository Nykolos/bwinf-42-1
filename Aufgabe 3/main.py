import copy
import sys
import os
from heapq import heappop, heappush

os.system("")

# Überprüfung auf richtige Eingabe
if len(sys.argv) != 2:
    print("Benutzung: main.py eingabe.txt")
    sys.exit(0)

# Datei einlesen
file = open(sys.argv[1])

# Datei in einzelne Zeilen unterteilen
lines = file.read().splitlines()

# Aus der obersten Zeile die Größe auslesen
# dimensions = lines[0]
lines.pop(0)

# Die Arrays definieren
labyrinth, current_level = list(), list()

# Jedes Feld in das Array labyrinth schreiben
for line in lines:
    # Prüfen ob Zeile Leer
    if line.strip():
        current_level.append(list(line.strip()))
    # Wenn leer, zweite Ebene
    else:
        labyrinth.append(current_level)
        current_level = list()
labyrinth.append(current_level)

path_field = copy.deepcopy(labyrinth)

# Start und End Punkt erstellen
start, end = None, None

# Start und End Punkt eintragen
for level, floor in enumerate(labyrinth):
    for x, row in enumerate(floor):
        for y, cell in enumerate(row):
            if cell == 'A':
                start = (x, y, level)
            if cell == 'B':
                end = (x, y, level)

# Überprüfung, ob es Punkt A und B gibt
if None in (start, end):
    print("Das Labyrinth muss einen Start- und Endpunkt haben")
    sys.exit(0)

# Bewegungsrichtungen: oben, unten, links, rechts
directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # (dx, dy)

# Länge und Breite des Labyrinths herausfinden
rows = len(labyrinth[0])
cols = len(labyrinth[0][0])

path_cost = float('inf')

# Alle Kombinationen in distances schreiben
distances = {(i, j, k): float('inf') for i in range(rows) for j in range(cols) for k in range(2)}
distances[start] = 0
queue = [(0, start)]  # (distance, node)

# Anzahl Stockwerkwechseln definieren
switch = 0

# Farbcodes für das Terminal
c = '\033[91m'
ende = '\033[0m'
b = '\033[94m'

# Variablen zur Wegspeicherung
path = []
prev = {start: None}


# Algorithmus zur Wegfindung
while queue:
    current_distance, (x, y, level) = heappop(queue)

    new_x, new_y = 0, 0

    # Für jede mögliche Bewegungsrichtung
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < rows and 0 <= new_y < cols and labyrinth[level][new_x][new_y] != '#':
            new_distance = current_distance + 1  # 1 Sekunde für benachbarten Zellen

            # Überprüfung, ob Weg ohne Stockwerkwechsel schneller wäre
            if new_distance < distances[(new_x, new_y, level)]:
                distances[(new_x, new_y, level)] = new_distance
                heappush(queue, (new_distance, (new_x, new_y, level)))
                prev[(new_x, new_y, level)] = (x, y, level)  # Aktualisiere den Vorgänger

    # Stockwerkswechsel
    new_level = 1 - level  # Wechsel zum anderen Stockwerk
    new_distance = current_distance + 3  # 3 Sekunden für Stockwerkswechsel

    if labyrinth[new_level][x][y] != '#':
        # Überprüfung, ob Weg mit Stockwerkwechsel schneller wäre
        if new_distance < distances[(x, y, new_level)]:
            distances[(x, y, new_level)] = new_distance
            heappush(queue, (new_distance, (x, y, new_level)))
            prev[(x, y, new_level)] = (x, y, level)  # Aktualisiere den Vorgänger

    if (x, y, level) == end:
        path_cost = distances[end]

        current = end
        while current is not None:
            path.append(current)
            current = prev[current]
        path = path[::-1]  # Umkehrung des Pfads, damit er vom Start zum Ziel verläuft

        # path enthält jetzt den Pfad von "start" zu "end"
        px, py = 0, 0
        for point in path:
            x, y, level = point

            p = labyrinth[level][x][y]
            po = labyrinth[1 - level][x][y]
            if p != "A" and p != "B":
                labyrinth[level][x][y] = c + '+' + ende  # Markiert einen Schritt im Labyrinth
            if px == x and py == y:
                switch += 1
                if p != "A" and p != "B":
                    labyrinth[level][x][y] = c + 'x' + ende  # Markiert ein Stockwerkwechsel im Labyrinth
                if po != "A" and po != "B" and po != b + "A" + ende:
                    labyrinth[1 - level][x][y] = c + 'x' + ende  # Markiert den alten Stockwerkwechsel im Labyrinth
            if p == "A" or p == "B":
                labyrinth[level][x][y] = b + p + ende  # Markiert die Punkte A und B blau

            px, py = x, y
        break


# Ausgabe des Weges
for level in labyrinth:
    for row in level:
        print(''.join(row))
    print()

# Zusatzinformationen
print("Man braucht: " + str(path_cost) + " Sekunden um von Punkt A zu Punkt B zu kommen mit " + str(switch) +
      " Stockwerkwechseln.")
