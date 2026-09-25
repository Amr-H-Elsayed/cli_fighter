import sys
import time

# ANSI Escape Sequences for styling & cursor movement
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

# ASCII Avatars (5 lines tall each)
AVATARS = {
    "p1": [
        "      e^^^s     ",
        "      &&&&&     ",
        "     &&>. <&    ",
        "  -e&&&&JG&&&_  ",
        " &&&&&&&&C&v&&& ",
        " &&&&&&&&&&&&&& ",
        "  #%& 7&&&&&& #f",
        "   s3  &&&&&& #f",
        "    f  #.4ykk  %",
        "       &&&  &&  ",
        "      &&&&  &&& ",
        "      &&&&  &&& "
    ],
    "p2": [
        "     s^^^e      ",
        "     &&&&&      ",
        "    &> .<&&     ",
        "  _&&&GJ&&&&e-  ",
        " &&&v&C&&&&&&&& ",
        " &&&&&&&&&&&&&& ",
        "f# &&&&&&7 &#%  ",
        "f# &&&&&&  3s   ",
        "%  kkX$&#  f    ",
        "  &&  &&&       ",
        " &&&  &&&&      ",
        " &&&  &&&&      "
    ]
}

def build_bar(current, maximum, length=15, fill_color=GREEN):
    # Generates a colored health/stamina bar for display in the CLI
    ratio = max(0, min(current / maximum, 1.0))
    filled_len = int(ratio * length)
    bar = "█" * filled_len + "░" * (length - filled_len)
    return f"[{fill_color}{bar}{RESET}] {current}/{maximum}"

def draw_battle_screen(p1, p2, combat_log="", lines_to_overwrite=0):
    """
    Renders the full game state.
    If lines_to_overwrite > 0, moves the cursor UP before drawing.
    """
    # 1. Clear previous render by moving cursor up N lines
    if lines_to_overwrite > 0:
        # \033[{lines_to_overwrite}A moves cursor UP by N lines
        sys.stdout.write(f"\033[{lines_to_overwrite}A")

    # 2. Prepare Health and Stamina Bars
    p1_hp_bar = build_bar(p1.hp, p1.max_hp, length=12, fill_color=GREEN)
    p2_hp_bar = build_bar(p2.hp, p2.max_hp, length=12, fill_color=GREEN)
    p1_st_bar = build_bar(p1.stamina, 50, length=12, fill_color=CYAN)
    p2_st_bar = build_bar(p2.stamina, 50, length=12, fill_color=CYAN)

    # 3. Assemble full frame (Line-by-Line)
    lines = []
    lines.append("==========================================================")
    lines.append(f"{BOLD}{p1.name:<25}{p2.name:>25}{RESET}")
    lines.append(f"HP: {p1_hp_bar:<25}  HP: {p2_hp_bar:>25}")
    lines.append(f"ST: {p1_st_bar:<25}  ST: {p2_st_bar:>25}")
    lines.append("----------------------------------------------------------")
    
    # Render Avatars side by side
    for i in range(len(AVATARS["p1"])):
        lines.append(f"  {AVATARS['p1'][i]:<20}         {AVATARS['p2'][i]:>20}  ")

    lines.append("==========================================================")
    
    # Padded log area to prevent ghost text overlapping
    padded_log = f"{YELLOW}{combat_log:<56}{RESET}"
    lines.append(f"LOG: {padded_log}")
    lines.append("==========================================================")

    # 4. Print entire block using carriage return
    frame = "\n".join(lines) + "\n"
    sys.stdout.write(frame)
    sys.stdout.flush()

    # Return total line count so main.py knows how many lines to jump up next time
    return len(lines)

def animate_attack(attacker_name):
    """Flashes action text briefly for visual impact."""
    sys.stdout.write(f"\r{RED}>>> {attacker_name} executes move! <<<{RESET}")
    sys.stdout.flush()
    time.sleep(1)