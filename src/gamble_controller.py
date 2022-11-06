class Gambler:
    def __init__(self):
        self.gold = 100
        self.bet = 0
        self.combatant_bet_on = None
    # checks if user would like to place a bet
    def place_bet(self, combatant1, combatant2):
        gamble = input('Would you like to place a bet? Please enter "yes" or "no": ')
        if 'y' in gamble.lower():
            while True:
                try:
                    self.combatant_bet_on = int(input("Who would you like to bet on? Please enter their seed number: "))
                    if (self.combatant_bet_on == combatant1.value.seed or
                        self.combatant_bet_on == combatant2.value.seed):
                        break
                    print("Sorry, that is not a valid input, please enter the seed number from the combatants above.")
                except ValueError:
                    print("Sorry, that is not a valid input, please enter the seed number from the combatants above.")
                
            while True:
                self.bet = int(input("Please enter the amount you would like to bet: "))
                if (self.bet <= self.gold) and (self.bet > 0):
                    self.gold -= self.bet
                    break
                print(f"Sorry, {self.bet} is not in range your gold range")
    # updates gold based on earnings from match
    def update_gold(self, winner):
        if self.bet == 0:
            return
        if winner.seed == self.combatant_bet_on:
            print(f"Congratulations, you won {self.bet * 2} gold from the fight!")
            self.gold += 2 * self.bet
            input("Please press enter to continue: ")
        else:
            input(f"Sorry, you lost {self.bet} gold.\nPlease press enter to continue: ")
        self.bet = 0
        self.combatant_bet_on = None

    def show_gold(self):
        print(f"Player gold: {self.gold}")

    def print_final_earnings(self):
        if self.gold < 100:
            print(f"Sorry, you lost out on some gold in this tournament. You lost {100 - self.gold} gold coins.")
        elif self.gold > 100:
            print(f"Congratulations, you made {self.gold - 100} gold coins extra from where you began!")
        else:
            print("You didn't earn any extra money but the good news is, you didn't loose any either!")
        print(f"Your final gold total is: {self.gold} gold coins.")