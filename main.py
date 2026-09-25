import os
from game import GameSession
from ui import draw_battle_screen, animate_attack

def main():
    os.system("")  # Enable ANSI escape sequences on Windows terminals
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
            current_player_name=game.current_player.name,
            lines_to_overwrite=rendered_lines
        )

        # 2. Check win state right after rendering
        winner = game.get_winner()
        if winner:
            print(f"\n{winner.name} DEFEATED {game.opponent.name}! {winner.name} WINS!")
            break

        # --- THIS IS WHERE THE CODE BLOCK GOES ---

        # 3. Action Prompt (1 line directly below the bottom box border)
        choice = input("Enter choice (1, 2, or 3) > ")

        # Optional animation cue (clears itself automatically now)
        animate_attack(game.current_player.name)

        # 4. Play turn and receive the combat log
        success, combat_log = game.play_turn(choice)

        # Exact lines to move up on next pass: ui_height + 1 input line
        rendered_lines = ui_height + 1

if __name__ == "__main__":
    main()