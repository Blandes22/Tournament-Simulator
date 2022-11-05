import os
import numpy as np
import commentator as commentator
from time import sleep
from combat import Combat
from gamble_controller import Gambler
from bracket import Bracket
from entrant import Entrant, PlaceHolder

class Tournament:
    def __init__(self, entrants):
        self.bracket = Bracket(entrants)
        self.level = self.bracket.depth
        self.current_level = 1
        self.battles_remaining_in_level = self.bracket.size - np.power(2, self.bracket.depth - 2)  # type: ignore
        self.combat = None
        self.combatant1 = None
        self.combatant2 = None
        self.gambler = Gambler()

    def initialize(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(
            "Hello and welcome to the Python Tournament Simulator! For this to work properly it is recommended that you run this program with the terminal in full screen.",
            "Throughout the tournament you are going to be shown the combatant's cards before each battle and you will have a chance to wager some gold coin on each battle.",
            "If you can successfully guess the outcome of the battle, you will recieve double the amount of money you put into the match. Otherwise, you will lose the money put in.",
            "The tournament consists of 16 combatants, each one fighting for the trophy. The Bracket will be displayed below for you to see.",
            sep="\n"
            )
        self.bracket.draw_bracket()

    def start_round(self):
        self.__get_combatants()
        self.draw_vs_screen()
        self.__bet()

    def __get_combatants(self):
        self.__traverse_bracket(self.bracket.tree.root)
        self.combat = Combat(self.combatant1, self.combatant2)

    def __traverse_bracket(self, node):
        if self.combatant1 or self.current_level > self.level:
            return
        self.current_level += 1
        if node.left.value.name == "TBD":
            self.__traverse_bracket(node.left)
        if node.right.value.name == "TBD":
            self.__traverse_bracket(node.right)
        if (
        isinstance(node.left.value, Entrant) and 
        isinstance(node.right.value, Entrant) and 
        self.current_level == self.level
        ):
            self.combatant1 = node.left
            self.combatant2 = node.right
        self.current_level -= 1
    
    def __bet(self):
        if self.gambler.gold >= 1:
            self.gambler.show_gold()
            self.gambler.place_bet(self.combatant1, self.combatant2)
        else:
            input("Sorry, you do not have any money to bet.\nPlease press enter to continue: ")

    def battle_phase(self):
        continue_combat = True
        self.__battle_begin_commentary()
        while continue_combat:
            dmg, atk_success, atk_type = self.combat.attack() # type: ignore
            sleep(3.5)
            self.__turn_commentary(atk_type, atk_success)
            continue_combat = self.combat.check_and_update(dmg) # type: ignore
        sleep(3.5)
        self.__match_end_commentary()

    def end_round(self):
        self.gambler.update_gold(self.combat.attacker) # type: ignore
        self.__update_bracket()

    def __update_bracket(self):
        self.battles_remaining_in_level -= 1 
        if self.battles_remaining_in_level == 0:
            self.level -= 1
            self.battles_remaining_in_level = (2 ** (self.level - 2))
        node = self.combatant1.previous # type: ignore
        node.value = self.combat.attacker # type: ignore
        if node.left.value == self.combat.defender: # type: ignore
            node.left.value = PlaceHolder("ELIMINATED")
        else:
            node.right.value = PlaceHolder("ELIMINATED")
        self.combatant1 = None
        self.combatant2 = None
        self.current_level = 1
        self.bracket.draw_bracket()

    def check_win(self):
        # root will only have a value of an Entrant object if the tournament is over.
        if isinstance(self.bracket.tree.root.value, Entrant): # type: ignore
            self.__draw_winner_screen()
            return True
        return False
    
    # eval() used in the functions below to treat commentary as an fstring
    def __battle_begin_commentary(self):
        print(eval('f"' + np.random.choice(commentator.first_strike_commentary) + '"'))

    def __turn_commentary(self, attack_type, attack_success):
        if attack_type == 'magic':
            if attack_success == 'critical':
                print(eval('f"' + np.random.choice(commentator.magic_crit) + '"'))
            if attack_success == 'hit':
                print(eval('f"' + np.random.choice(commentator.magic_hit) + '"'))
            if attack_success == 'miss':
                print(eval('f"' + np.random.choice(commentator.magic_miss) + '"'))
        if attack_type == "physical":
            if attack_success == 'critical':
                print(eval('f"' + np.random.choice(commentator.physical_crit) + '"'))
            if attack_success == 'hit':
                print(eval('f"' + np.random.choice(commentator.physical_hit) + '"'))
            if attack_success == 'miss':
                print(eval('f"' + np.random.choice(commentator.physical_miss) + '"'))
    
    def __match_end_commentary(self):
        print(eval('f"' + np.random.choice(commentator.winner_commentary) + '"'))

    def draw_vs_screen(self):
        entrant = self.combatant1.value # type: ignore
        entrant2 = self.combatant2.value # type: ignore
        print("Please examine the combatant's cards below and determine if you would like to wager any gold on the battle.\n")
        print(''.rjust(30), '* ' * 14, ''.rjust(41), '* ' * 14)
        print(
                ''.rjust(30), '*', (" Name: " + entrant.name).ljust(23), 
                '*', ''.rjust(42), '*', (" Name: " + entrant2.name).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Seed: " + str(entrant.seed)).ljust(23), '*', 
                ''.rjust(42), '*', (" Seed: " + str(entrant2.seed)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', ''.center(23, '-'), '*', ''.rjust(42), '*', 
                ''.center(23, '-'), '*'
            )
        print(
                ''.rjust(30), '*', ''.ljust(23), '*', 
                ''.rjust(42), '*', ''.ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Health: " + str(entrant.health)).ljust(23), 
                '*', ''.rjust(42), '*', (" Health: " + str(entrant2.health)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Physical Attack: " + 
                str(entrant.phys_atk)).ljust(23),'*', ''.rjust(42), '*', 
                (" Physical Attack: " + str(entrant2.phys_atk)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Magic Attack: " + str(entrant.mag_atk)).ljust(23),
                '*', r"____   ____       ".rjust(30), ''.rjust(11), '*', 
                (" Magic Attack: " + str(entrant2.mag_atk)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Physical Defense: " + str(entrant.phys_def)).ljust(23),
                '*', r"\   \ /   / _____ ".rjust(30), ''.rjust(11), '*', 
                (" Physical Defense: " + str(entrant2.phys_def)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Magic Defense: " + str(entrant.mag_def)).ljust(23), 
                '*', r" \   V   //  ___/ ".rjust(30), ''.rjust(11), '*', 
                (" Magic Defense: " + str(entrant2.mag_def)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', (" Speed: " + str(entrant.speed)).ljust(23), 
                '*', r" \     / \___  \ ".rjust(30), ''.rjust(11), '*', 
                (" Speed: " + str(entrant2.speed)).ljust(23), '*'
            )
        print(
                ''.rjust(30), '*', ''.ljust(23), '*', r"   \___/  /_____/ ".rjust(30),
                ''.rjust(11), '*', ''.ljust(23), '*'
            )
        print(''.rjust(30), '* ' * 14, ''.rjust(41), '* ' * 14)

    def __draw_winner_screen(self):
        entrant = self.bracket.tree.root.value  # type: ignore
        print(f"Congratulations {entrant.name}! You are the winner of todays tournament! Please speak to the tournament officials to collect your prize!") # type: ignore
        print(
            '  __      __   __                                     \n',
            '/  \    /  \ |__|   ____     ____    _____    ______ \n',
            '\   \/\/   / |  |  /    \   /    \  /  __ \  |_  ___\\\n',
            ' \        /  |  | |   |  \ |   |  \ \  ___/   |  |   \n',
            '  \__/\__/   |__| |___|__/ |___|__/  \____)   |__|   \n',
        )
        print(''.rjust(13), '* ' * 14)
        print(''.rjust(13), '*', (" Name: " + entrant.name).ljust(23), '*')        # type: ignore
        print(''.rjust(13), '*', (" Seed: " + str(entrant.seed)).ljust(23), '*')   # type: ignore
        print(''.rjust(13), '*', ''.center(23, '-'), '*')
        print(''.rjust(13), '*', ''.ljust(23), '*')
        print(''.rjust(13), '*', (" Health: " + str(entrant.health)).ljust(23), '*') # type: ignore
        print(''.rjust(13), '*', (" Physical Attack: " + str(entrant.phys_atk)).ljust(23), '*') # type: ignore
        print(''.rjust(13), '*', (" Magic Attack: " + str(entrant.mag_atk)).ljust(23), '*') # type: ignore
        print(''.rjust(13), '*', (" Physical Defense: " + str(entrant.phys_def)).ljust(23),'*') # type: ignore
        print(''.rjust(13), '*', (" Magic Defense: " + str(entrant.mag_def)).ljust(23), '*' ) # type: ignore
        print(''.rjust(13), '*', (" Speed: " + str(entrant.speed)).ljust(23), '*') # type: ignore
        print(''.rjust(13), '*', ''.ljust(23), '*')
        print(''.rjust(13), '* ' * 14)
        self.gambler.print_final_earnings()