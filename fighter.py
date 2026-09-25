
class Fighter:
    def __init__ (self, name, hp=100, stamina=50):
        self.name = name
        self.hp = hp
        self.stamina = stamina

    def normal_attack(self, target):
        # something something
        
    def take_damage(self, amount):
        self.hp -= amount
        