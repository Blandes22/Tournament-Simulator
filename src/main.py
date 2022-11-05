from tournament_controller import Tournament
from random import randint
from entrant import Entrant
import os

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")

def main():
    with open(os.path.join(ROOT_DIR, "assets", "data", "names.txt"), 'r') as file:
        names = file.read()
        names = names.split('\n')
    entrants = []
    entrant_names = []
    # create 16 different entrants all with unique names
    while len(entrant_names) < 16:
        temp = names[randint(0, len(names) - 1)]
        if temp not in entrant_names: 
            entrant_names.append(temp)
            entrant = Entrant(temp, len(entrant_names))
            entrants.append(entrant)

    tournament = Tournament(entrants)
    tournament.initialize()
    input("Please press enter to continue: ")
    while True: 
        tournament.start_round()
        tournament.battle_phase()
        tournament.end_round()
        if tournament.check_win():
            break

if __name__ == '__main__':
    main()
