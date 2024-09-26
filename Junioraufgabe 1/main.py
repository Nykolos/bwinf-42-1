import sys

if len(sys.argv) != 2:
    print("Benutzung: main.py eingabe.txt")
    sys.exit(0)

file = open(sys.argv[1], "r")

lines = file.read().splitlines()

# Auslesen der Anzahl Tüten und Varianten
count_bag = lines[0]
count_variants = lines[1]

# entfernen dieser aus dem dokument
lines.pop(0)
lines.pop(0)

# Aufteilung der Spielzeuge auf alle Tüten
variants = list()
for variant in lines:
    if variant == '':
        break

    count, remaining = divmod(int(variant), int(count_bag))
    obj = [count, remaining]
    variants.append(obj)

a = list()
for obj in variants:
    a.append(obj[1])

wv = list()

# Aufteilung der restlichen Spielzeuge
u = 0
for i in range(int(count_variants)):
    while a[i] > 0:
        a[i] -= 1
        y = [u, i]
        wv.append(y)
        u += 1
        if u > int(count_bag) - 1:
            u -= int(count_bag)

# Ausgabe der Variablen
x = ""
for i, variant in enumerate(variants):
    if variant[0] != 0:
        x += str(variant[0]) + "x Spielzeug " + str(i + 1) + ", "
if x != "":
    print("In jede Wundertüte müssen " + x[:-2])
for i in range(int(count_bag)):
    el = list()
    for item in wv:
        if item[0] == i:
            el.append(item[1])
    ml = list()
    for variant in lines:
        ml.append(0)
    for item in el:
        ml[int(item)] += 1
    x = ""
    for y, itm in enumerate(ml):
        if itm > 0:
            x += str(itm) + "x Spielzeug " + str(y + 1) + ", "
    if x != "":
        print("In Wundertüte " + str(i + 1) + " müssen zusätzlich " + x)
