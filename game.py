from fighter import Fighter

class GameSession:
    def __init__ (self, p1_name, p2_name):
        self.player1 = Fighter(p1_name)
        self.player2 = Fighter(p2_name)

        # track active turn (start with player 1)
        self.current_player = self.player1
        self.opponent = self.player2

    def switch_turns(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
            self.opponent = self.player1
        else:
            self.current_player = self.player1
            self.opponent = self.player2

    def play_turn(self, choice):
        if choice == "1":
            success, msg = self.current_player.normal_attack(self.opponent)
        elif choice == "2":
            success, msg = self.current_player.critical_attack(self.opponent)
        elif choice == "3":
            success, msg = self.current_player.heal()
        else:
            return False, "Invalid choice! Please select 1, 2, or 3."

        if success:
            self.switch_turns()

        return success, msg

    # Inside GameSession in game.py:
    def get_winner(self):
        if self.player1.hp <= 0:
            return self.player2
        elif self.player2.hp <= 0:
            return self.player1
        return None