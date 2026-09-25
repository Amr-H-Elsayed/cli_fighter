from fighter import Fighter

class GameSession:
    def __init__(self, p1_name, p2_name):
        self.player1 = Fighter(p1_name)
        self.player2 = Fighter(p2_name)

        self.current_player = self.player1
        self.opponent = self.player2
        
        # Track if the current opponent is exposed to a Finish Him strike
        self.opponent_exhausted = False

    def switch_turns(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.opponent = self.player1
        else:
            self.current_player = self.player1
            self.opponent = self.player2

    def play_turn(self, choice):
        # Store opponent HP before attack to measure normal damage
        pre_attack_hp = self.opponent.hp

        if choice == "1":
            success, msg = self.current_player.normal_attack(self.opponent)
        elif choice == "2":
            success, msg = self.current_player.critical_attack(self.opponent)
        elif choice == "3":
            success, msg = self.current_player.heal()
        else:
            return False, "Invalid choice! Please select 1, 2, or 3."

        if success:
            # If the opponent was exhausted and an attack hit, boost the damage to 100
            if self.opponent_exhausted and choice in ["1", "2"] and self.opponent.hp < pre_attack_hp:
                self.opponent.hp = 0  # 100 damage instantly finishes them
                msg = f"FINISH HIM! {self.current_player.name} landed a lethal 100 DMG blow!"
                self.opponent_exhausted = False  # Reset flag

            # Check if the player who just acted ran out of stamina
            if self.current_player.stamina <= 0:
                exhausted_name = self.current_player.name
                
                # Switch turn so opponent can finish them
                self.switch_turns()
                
                self.current_player.stamina = 100  # Give attacker full stamina
                self.opponent_exhausted = True     # Mark opponent as vulnerable
                
                msg = f"{exhausted_name} is completely exhausted! FINISH HIM!"
            else:
                self.switch_turns()

        return success, msg

    def get_winner(self):
        if self.player1.hp <= 0:
            return self.player2
        elif self.player2.hp <= 0:
            return self.player1
        return None