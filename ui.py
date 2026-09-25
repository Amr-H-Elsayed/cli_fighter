import sys
import time

# ANSI Escape Sequences for styling & cursor movement
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

# ASCII Avatars
AVATARS = {
    "p1": [
        "      e^^^s     ",
        "      &&&&&     ",
        "     &&>. <&    ",
        "  -e&&&&JG&&&_  ",
        " &&&&&&&&C&v&&& ",
        " &&&&&&&&&&&&&&&",
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
        "&&&&&&&&&&&&&&& ",
        "f# &&&&&&7 &#%  ",
        "f# &&&&&&  3s   ",
        "%  kkX$&#  f    ",
        "  &&  &&&       ",
        " &&&  &&&&      ",
        " &&&  &&&&      "
    ]
}

WIDTH = 64  # Inner width boundary

def format_row(content: str) -> str:
    """Wraps text in side borders and pads spacing to fit the box precisely."""
    import re
    # Calculate visible length ignoring ANSI color escape characters
    visible_len = len(re.sub(r'\033\[[0-9;]*m', '', content))
    padding = max(0, WIDTH - visible_len)
    return f"║ {content}{' ' * padding} ║"

def build_bar(current, maximum, length=12, fill_color=GREEN):
    ratio = max(0, min(current / maximum, 1.0))
    filled_len = int(ratio * length)
    bar = "█" * filled_len + "░" * (length - filled_len)
    return f"[{fill_color}{bar}{RESET}] {current}/{maximum}"

def draw_battle_screen(p1, p2, combat_log="", current_player_name="", lines_to_overwrite=0):
    if lines_to_overwrite > 0:
        sys.stdout.write(f"\033[{lines_to_overwrite}A\033[0J")

    p1_hp_bar = build_bar(p1.hp, p1.max_hp, length=12, fill_color=GREEN)
    p2_hp_bar = build_bar(p2.hp, p2.max_hp, length=12, fill_color=GREEN)
    p1_st_bar = build_bar(p1.stamina, 100, length=12, fill_color=CYAN)
    p2_st_bar = build_bar(p2.stamina, 100, length=12, fill_color=CYAN)

    lines = []
    # Top Border
    lines.append("╔" + "═" * (WIDTH + 2) + "╗")
    
    # Names & Stats
    lines.append(format_row(f"{BOLD}{p1.name:<28}{p2.name:>28}{RESET}"))
    lines.append(format_row(f"HP: {p1_hp_bar:<24} HP: {p2_hp_bar:>24}"))
    lines.append(format_row(f"ST: {p1_st_bar:<24} ST: {p2_st_bar:>24}"))
    
    # Divider
    lines.append("╠" + "═" * (WIDTH + 2) + "╣")
    
    # Avatars
    for i in range(len(AVATARS["p1"])):
        lines.append(format_row(f"  {AVATARS['p1'][i]:<20}         {AVATARS['p2'][i]:>20}  "))

    # Divider
    lines.append("╠" + "═" * (WIDTH + 2) + "╣")
    
    # Combat Log Area
    lines.append(format_row(f"LOG: {YELLOW}{combat_log:<52}{RESET}"))
    
    # Divider
    lines.append("╠" + "═" * (WIDTH + 2) + "╣")

    # Action Menu inside the box
    lines.append(format_row(f"{BOLD}{current_player_name}'s turn! Choose action:{RESET}"))
    lines.append(format_row("1. Normal Attack (5 ST)   2. Critical Attack (15 ST)"))
    lines.append(format_row("3. Heal (20 ST)"))
    
    # Bottom Border
    lines.append("╚" + "═" * (WIDTH + 2) + "╝")

    frame = "\n".join(lines) + "\n"
    sys.stdout.write(frame)
    sys.stdout.flush()

    return len(lines)

def animate_attack(attacker_name):
    # Print animation message, wait 0.5s, then erase the line completely using \r and \033[K
    sys.stdout.write(f"\r{GREEN}>>> {attacker_name} executes move! <<<{RESET}")
    sys.stdout.flush()
    time.sleep(0.5)
    # Clear line so it doesn't mess up line counts for draw_battle_screen
    sys.stdout.write("\r\033[K")
    sys.stdout.flush()