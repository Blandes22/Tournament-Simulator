from random import randint, shuffle

class Combat:
    def __init__(self, entrant1, entrant2):
        self.attacker, self.defender = self.__set_first_turn(entrant1.value, entrant2.value)
        self.entrant1 = entrant1
        self.entrant2 = entrant2
        self.e1health = entrant1.value.health
        self.e2health = entrant2.value.health

    # determines which combatant goes first based on chance and speed
    def __set_first_turn(self, entrant1, entrant2):
        # get roll for both combatants
        total = entrant1.speed + entrant2.speed
        entrant1_roll = self.__initiative_roll(entrant1, total)
        entrant2_roll = self.__initiative_roll(entrant2, total)
        # sets combatant with higher roll to go first
        if entrant1_roll > entrant2_roll:
            return entrant1, entrant2
        elif entrant2_roll > entrant1_roll:
            return entrant2, entrant1
        # if both rolls have the same value...
        else:
            # check for speeds on both combatants and allow the one with higher speed to go first
            if entrant1.speed > entrant2.speed:
                return entrant1, entrant2
            elif entrant2.speed > entrant1.speed:
                return entrant2, entrant1
        # if both rolls and both speeds are the same
        # randomize which combatant goes first
        temp = [entrant1, entrant2]
        shuffle(temp)
        return temp[0], temp[1]
    
    def __initiative_roll(self, entrant, total):
        # gives advantage to combatant with higher speed but still allows 
        # chance of combatant with lower speed to go first
        roll = (entrant.speed / total)
        roll *= randint(1, 10)
        return roll 

    # checks if defender has taken enough damage to be defeated
    def check_and_update(self, damage):
        # updated defender health based on attack damage given
        self.defender.update_health(damage)
        if self.defender.health < 0:
            # if defender is defeated, restore attackers health to max
            if self.entrant1.value == self.attacker:
                self.attacker.health = self.e1health
            else:
                self.attacker.health = self.e2health
            return False
        # otherwise, reverse rolls so defender is now attacker and vice versa
        self.attacker, self.defender = self.defender, self.attacker
        return True

    def attack(self):
        # set roll to determine success of attack
        roll = randint(1, 10)
        attack_success = self.attacker.calculate_roll_success(roll)
        attack_type = self.attacker.calculate_attack_type(self.defender.mag_def, self.defender.phys_def)
        damage = self.attacker.calculate_damage(roll, attack_type, self.defender.mag_def, self.defender.phys_def)
        
        # prevents negative damge, so attacker does not give health to defender
        # alse sets attack type to miss if damage is less than 1
        if damage < 1:
            attack_success = 'miss'
            damage = 0
        # damage used to update health of defender
        # attack_success and attack_type used for commentary
        return damage, attack_success, attack_type