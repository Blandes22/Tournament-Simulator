from random import randint

class Entrant:
    def __init__(self, name: str, seed):
        self.name = name
        self.seed = seed
        self.phys_atk = randint(30,100)
        self.mag_atk = randint(30,100)
        self.phys_def = randint(1,10)
        self.mag_def = randint(1,10)
        self.speed = randint(1,10)
        self.health = (randint(100, 200) // 10) * 10

    def update_health(self, dmg):
        self.health -= dmg

    # checks if roll gives attacker a critical, standard, or miss
    def calculate_roll_success(self, roll):
        if roll == 10:
            success = 'critical'
        elif roll == 1:
            success = 'miss'
        else:
            success = 'hit'
        return success

    def calculate_attack_type(self, defender_mag_def, defender_phys_def):
        # take arbitrary weighted chance of mag attack and phys attack based on attacker and defender stats
        mag_weight = self.mag_atk - (defender_mag_def * 2)
        phys_weight = self.phys_atk - (defender_phys_def * 2)
        total = mag_weight + phys_weight
        # find chance of attacker doing a magic attack
        mag_chance = ((mag_weight / total) * 100) // 1
        # roll to see if attack will be magic or physical
        check = randint(1, 100)
        if check <= mag_chance:
            return "magic"
        else:
            return "physical"

    def calculate_damage(self, roll, atk_type, defender_mag_def, defender_phys_def):
        # check attack type then set atk to said type
        if atk_type == "magic":
            atk = self.mag_atk
            defense = defender_mag_def
        else:
            atk = self.phys_atk
            defense = defender_phys_def
        # critical attack
        if roll == 10:
            damage = atk - defense
        # standard attack
        elif roll < 10 and roll > 1:
            damage = (atk * 0.75) - (defense * 2)
        # miss
        else: 
            damage = 0
        # returns damage as an int preventing float damage
        return int(damage)

# PlaceHolder class used for building bracket
class PlaceHolder:
    def __init__(self, name):
        self.name = name