from random import randint, shuffle

class Combat:
    def __init__(self, entrant1, entrant2):
        self.attacker, self.defender = self.__set_first_turn(entrant1.value, entrant2.value)
        self.entrant1 = entrant1
        self.entrant2 = entrant2
        self.e1health = entrant1.value.health
        self.e2health = entrant2.value.health

    def __set_first_turn(self, entrant1, entrant2):
        total = entrant1.speed + entrant2.speed
        entrant1_roll = self.__initiative_roll(entrant1, total)
        entrant2_roll = self.__initiative_roll(entrant2, total)
        if entrant1_roll > entrant2_roll:
            return entrant1, entrant2
        elif entrant2_roll > entrant1_roll:
            return entrant2, entrant1
        else:
            if entrant1.speed > entrant2.speed:
                return entrant1, entrant2
            elif entrant2.speed > entrant1.speed:
                return entrant2, entrant1
        temp = [entrant1, entrant2]
        shuffle(temp)
        return temp[0], temp[1]
    
    def __initiative_roll(self, entrant, total):
        roll = (entrant.speed / total)
        roll *= randint(1, 10)
        return roll 

    def check_and_update(self, damage):
        self.defender.update_health(damage)
        if self.defender.health < 0:
            if self.entrant1.value == self.attacker:
                self.attacker.health = self.e1health
            else:
                self.attacker.health = self.e2health
            return False
        self.attacker, self.defender = self.defender, self.attacker
        return True

    def attack(self):
        roll = randint(1, 10)
        attack_success = self.attacker.calculate_roll_success(roll)
        attack_type = self.attacker.calculate_attack_type(
            self.defender.mag_def, self.defender.phys_def
            )
        damage = self.attacker.calculate_damage(roll, attack_type, self.defender.mag_def, self.defender.phys_def)
        if damage < 1:
            attack_success = 'miss'
            damgae = 0
        return damage, attack_success, attack_type