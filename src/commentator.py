import os

# sets root directory for ease of access to commentary.py
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")

# takes contents of commentary.txt and stores it as a single list
with open(os.path.join(ROOT_DIR, "assets", "data", 'commentary.txt'), 'r') as file:
    string_stream = file.read()
    string_stream = string_stream.split('\n')

# initialize empty lists
first_strike_commentary = []
magic_crit = []
magic_hit = []
magic_miss = []
physical_crit = []
physical_hit = []
physical_miss = []
winner_commentary = []

# stores commentary in appropriate lists based on start of the string
for i in string_stream:
    if ':_' in i:
        continue
    if i[:13] == 'first strike:':
        first_strike_commentary.append(i[13:])
    elif i[:8] == 'mag:hit:':
        magic_hit.append(i[8:])
    elif i[:9] == 'mag:miss:':
        magic_miss.append(i[9:])
    elif i[:13] == 'mag:critical:':
        magic_crit.append(i[13:])
    elif i[:9] == 'phys:hit:':
        physical_hit.append(i[9:])
    elif i[:10] == 'phys:miss:':
        physical_miss.append(i[10:])
    elif i[:14] == 'phys:critical:':
        physical_crit.append(i[14:])
    elif i[:4] == 'end:':
        winner_commentary.append(i[4:])