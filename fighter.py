import random

class Fighter:
    def __init__ (self, name, hp=100, stamina=100):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.stamina = stamina

    def normal_attack(self, target):
        stamina_cost = 5

        # Check if stamina is Sufficient first
        if self.stamina < stamina_cost:
            return False, f"{self.name} doesn't have enough stamina!"
        else:
            self.stamina -= stamina_cost

        # Roll Hit Chance (80%)
        hit_chance = 0.8  
        
        if random.random() < hit_chance:
            damage = random.randint(8, 15)  # damage range
            target.take_damage(damage)
            msg = f"{self.name} hit {target.name} with {damage} damage!"
        else:
            msg = f"{self.name}'s attack missed! lol"
            
        return True, msg
        
    def take_damage(self, amount):
        self.hp -= amount
        # Ensures hp doesn't drop below 0
        if self.hp < 0:
            self.hp = 0

    def critical_attack(self, target):
        stamina_cost = 15

        if self.stamina < stamina_cost:
            return False, f"{self.name} doesn't have enough stamina!"
        
        self.stamina -= stamina_cost
        hit_chance = 0.45

        if random.random() < hit_chance:
            damage = random.randint(25, 35)
            target.take_damage(damage)
            msg = f"{self.name} CRITICALLY HIT {target.name} FOR {damage} DAMAGE!"
        else:
            msg = f"{self.name}'s critical attack missed! lol"
            
        return True, msg

    def heal(self):
        stamina_cost = 20

        if self.stamina < stamina_cost:
            return False, f"{self.name} doesn't have enough stamina!"
        
        if self.hp >= self.max_hp:
            return False, f"{self.name} is already at full health!"
        
        self.stamina -= stamina_cost
        heal_amount = random.randint(15, 25)
        self.hp += heal_amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        msg = f"{self.name} healed for {heal_amount} HP!"
        return True, msg

def finish_him(self, target):
    """Special finishing move when opponent is exhausted."""
    damage = 100  # Guaranteed damage to finish off
    target.take_damage(damage)
    msg = f"{self.name} FINISHES {target.name} WITH {damage} DAMAGE!"
    return True, msg