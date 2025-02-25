import random
from playsound import playsound

# Game Constants
SHIP_SIZES = [5, 4, 3, 3, 2]
SHIP_NAMES = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
MAP_SIZE = 10
ROW_LABELS = "ABCDEFGHIJ"

# Initialize Game Boards
def create_board(size):
    return [["_"] * size for _ in range(size)]

def print_board(board, show_ships=False):
    """Prints the game board with optional ship visibility."""
    print("  " + " ".join(str(i + 1) for i in range(MAP_SIZE)))
    for i, row in enumerate(board):
        print(ROW_LABELS[i] + " " + " ".join(row if show_ships else ["X" if cell == "S" else cell for cell in row]))

# Validate ship placement
def is_valid_placement(board, row, col, size, orientation):
    """Checks if a ship can be placed at the given coordinates."""
    if orientation == "