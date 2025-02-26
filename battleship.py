import random
from playsound import playsound

# Game Constants
SHIP_SIZES = [5, 4, 3, 3, 2]
SHIP_NAMES = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
MAP_SIZE = 10
ROW_LABELS = "ABCDEFGHIJ"

# Get player name
while True:
    user_name = input("Enter your name: ")
    if user_name:
        print(f"Welcome to the Battleship game, {user_name}!")
        break
    else:
        print("Please enter your name.")

# Initialize boards
player_board = [["_"] * MAP_SIZE for _ in range(MAP_SIZE)]
comp_board = [["_"] * MAP_SIZE for _ in range(MAP_SIZE)]
dummy_board = [["_"] * MAP_SIZE for _ in range(MAP_SIZE)]

player_ships = []
comp_ships = []
player_sunk_ships = []
comp_sunk_ships = []

# Display initial board
print("  " + " ".join(str(i + 1) for i in range(MAP_SIZE)))
for i, row in enumerate(player_board):
    print(ROW_LABELS[i] + " " + " ".join(row))

# Player places ships
for size, name in zip(SHIP_SIZES, SHIP_NAMES):
    while True:
        try:
            row = ROW_LABELS.index(input(f"Enter the row for {name} (A-J): ").upper())
            col = int(input(f"Enter the column for {name} (1-10): ")) - 1
            orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()

            if orientation not in ["H", "V"]:
                print("Invalid orientation. Enter H or V.")
                continue

            valid = True
            if orientation == "H":
                if col + size > MAP_SIZE or any(player_board[row][col + i] != "_" for i in range(size)):
                    valid = False
            else:
                if row + size > MAP_SIZE or any(player_board[row + i][col] != "_" for i in range(size)):
                    valid = False

            if valid:
                ship_positions = []
                for i in range(size):
                    if orientation == "H":
                        player_board[row][col + i] = "S"
                        ship_positions.append((row, col + i))
                    else:
                        player_board[row + i][col] = "S"
                        ship_positions.append((row + i, col))
                player_ships.append((name, size, ship_positions))

                print("  " + " ".join(str(i + 1) for i in range(MAP_SIZE)))
                for i, row in enumerate(player_board):
                    print(ROW_LABELS[i] + " " + " ".join(row))
                break
            else:
                print("Invalid placement. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

# Computer places ships randomly
for size, name in zip(SHIP_SIZES, SHIP_NAMES):
    while True:
        row = random.randrange(0, MAP_SIZE)
        col = random.randrange(0, MAP_SIZE)
        orientation = "H" if random.randrange(2) == 0 else "V"

        valid = True
        if orientation == "H":
            if col + size > MAP_SIZE or any(comp_board[row][col + i] != "_" for i in range(size)):
                valid = False
        else:
            if row + size > MAP_SIZE or any(comp_board[row + i][col] != "_" for i in range(size)):
                valid = False

        if valid:
            ship_positions = []
            for i in range(size):
                if orientation == "H":
                    comp_board[row][col + i] = "S"
                    ship_positions.append((row, col + i))
                else:
                    comp_board[row + i][col] = "S"
                    ship_positions.append((row + i, col))
            comp_ships.append((name, size, ship_positions))
            break

# Game loop
player_hits = 0
comp_hits = 0
while True:
    # Player's turn
    try:
        row = ROW_LABELS.index(input("Enter your row (A-J): ").upper())
        col = int(input("Enter your col (1-10): ")) - 1

        if comp_board[row][col] == "S":
            comp_board[row][col] = "X"
            dummy_board[row][col] = "X"
            print("Computer: Ship has been hit!")

            ship_sunk = False
            for name, size, positions in comp_ships:
                if all(comp_board[r][c] == "X" for r, c in positions):
                    if name not in comp_sunk_ships:
                        comp_sunk_ships.append(name)
                        print(f"Computer: {name} (size {size}) has been sunk!")
                        playsound('ship-hit-and-sunk.mp3')
                        print(f"Computer's sunk ships: {', '.join(comp_sunk_ships)}")
                        ship_sunk = True
                        break
            if not ship_sunk:
                playsound('ship-hit.mp3')

            player_hits += 1
        elif comp_board[row][col] in ["*", "X"]:
            print("You have already attacked this position. Try again.")
            continue
        else:
            comp_board[row][col] = "*"
            dummy_board[row][col] = "*"
            print("Missed!")
            playsound('ship-miss.mp3')
    except ValueError:
        print("Invalid input. Try again.")
        continue

    if player_hits == sum(SHIP_SIZES):
        print("All ships have been sunk!")
        print("Player has won - game over")
        playsound('win.wav')
        break

    # Computer's turn
    while True:
        row = random.randrange(0, MAP_SIZE)
        col = random.randrange(0, MAP_SIZE)
        if player_board[row][col] not in ["*", "X"]:
            break

    print("Computer has selected coordinates", ROW_LABELS[row], col + 1)

    if player_board[row][col] == "S":
        player_board[row][col] = "X"
        print("Player: Ship has been hit!")

        ship_sunk = False
        for name, size, positions in player_ships:
            if all(player_board[r][c] == "X" for r, c in positions):
                if name not in player_sunk_ships:
                    player_sunk_ships.append(name)
                    print(f"Player: {name} (size {size}) has been sunk!")
                    playsound('ship-hit-and-sunk.mp3')
                    print(f"Player's sunk ships: {', '.join(player_sunk_ships)}")
                    ship_sunk = True
                    break
        if not ship_sunk:
            playsound('ship-hit.mp3')

    else:
        player_board[row][col] = "*"
        print("Missed!")
        playsound('ship-miss.mp3')

    if comp_hits == sum(SHIP_SIZES):
        print("All ships have been sunk!")
        print("Computer has won - game over")
        playsound('loss.wav')
        break

    # Display Boards
    print(f"\nPlayer {user_name}'s Board")
    print("  " + " ".join(str(i + 1) for i in range(MAP_SIZE)))
    for i, row in enumerate(player_board):
        print(ROW_LABELS[i] + " " + " ".join(row))

    print("\nComputer Board (Hidden)")
    print("  " + " ".join(str(i + 1) for i in range(MAP_SIZE)))
    for i, row in enumerate(dummy_board):
        print(ROW_LABELS[i] + " " + " ".join(row))
