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
        # 1. GUARANTEED FINISH HIM: If opponent is exhausted, ANY attack choice automatically executes them!
        if self.opponent_exhausted and choice in ["1", "2"]:
            self.opponent.hp = 0
            self.opponent_exhausted = False
            
            msg = f"FINISH HIM! {self.current_player.name} landed a FINISHER on {self.opponent.name}!"
            return True, msg

        # 2. Normal move logic when not in a finisher state
        if choice == "1":
            success, msg = self.current_player.normal_attack(self.opponent)
        elif choice == "2":
            success, msg = self.current_player.critical_attack(self.opponent)
        elif choice == "3":
            success, msg = self.current_player.heal()
        else:
            return False, "Invalid choice! Please select 1, 2, or 3."

        # 3. Check if the player who just acted ran out of stamina
        if success:
            if self.current_player.stamina <= 0:
                exhausted_name = self.current_player.name
                
                # Switch turn so the opponent gets the guaranteed strike
                self.switch_turns()
                
                self.current_player.stamina = 100  # Give attacker full stamina
                self.opponent_exhausted = True     # Mark opponent as defenseless
                
                msg = f"{exhausted_name} is exhausted! FINISH HIM!"
            else:
                self.switch_turns()

        return success, msg

    def get_winner(self):
        if self.player1.hp <= 0:
            return self.player2
        elif self.player2.hp <= 0:
            return self.player1
        return None