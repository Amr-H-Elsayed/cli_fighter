from game import GameSession
from ui import draw_battle_screen, animate_attack

def main():
    print("Welcome to the CLI War Game!")
    p1_name = input("Enter name for Player 1: ")
    p2_name = input("Enter name for Player 2: ")

    game = GameSession(p1_name, p2_name)

    # Initialize variables needed before loop starts
    combat_log = "The battle begins!"
    rendered_lines = 0

    while True:
        # 1. Render/Overwrite the main UI block
        ui_height = draw_battle_screen(
            game.player1, 
            game.player2, 
            combat_log, 
            lines_to_overwrite=rendered_lines
        )

        # 2. Check win state right after rendering
        winner = game.get_winner()
        if winner:
            print(f"\n{winner.name} DEFEATED {game.opponent.name}! {winner.name} WINS!")
            break

        # 3. Action Menu (Printed cleanly below the UI block - exactly 5 lines printed)
        print(f"\n{game.current_player.name}'s turn! Choose action:")
        print("1. Normal Attack (Cost: 5 Stamina)")
        print("2. Critical Attack (Cost: 15 Stamina)")
        print("3. Heal (Cost: 20 Stamina)")

        choice = input("Enter your choice (1, 2, or 3): ")

        # Calculate TOTAL lines printed in this frame cycle
        # ui_height + 5 lines (blank line + header + 3 options + input line)
        rendered_lines = ui_height + 5

        # Optional animation cue
        animate_attack(game.current_player.name)

        # 4. Play turn and receive the exact combat_log string returned from game.py
        success, combat_log = game.play_turn(choice)

if __name__ == "__main__":
    main()