from random import randrange, choice
from playsound import playsound

ship_sizes = [5, 4, 3, 3, 2]
ship_names = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
map_size = 10
row_labels = "ABCDEFGHIJ"

while True:
    user_name = input("Enter your name: ")
    if user_name:
        print(f"Welcome to the battleship game {user_name}!")
        break
    else:
        print("Please enter your name.")

player_board = [["_"] * map_size for _ in range(map_size)]
comp_board = [["_"] * map_size for _ in range(map_size)]
dummy_board = [["_"] * map_size for _ in range(map_size)]

player_ships = []
comp_ships = []

player_sunk_ships = []
comp_sunk_ships = []

print("  " + " ".join(str(i + 1) for i in range(len(player_board[0]))))
for i, row in enumerate(player_board):
    print(row_labels[i] + " " + " ".join(row))

# player ship placement
for size, name in zip(ship_sizes, ship_names):
    while True:
        try:
            row = row_labels.index(input(f"Enter the row for {name} (A-J): ").upper())
            col = int(input(f"Enter the column for {name} (1-10): ")) - 1
            orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
            if orientation in ["H", "V"]:
                valid = True
                if orientation == "H":
                    if col + size > map_size:
                        valid = False
                    for i in range(size):
                        if col + i >= map_size or player_board[row][col + i] != "_":
                            valid = False
                else:
                    if row + size > map_size:
                        valid = False
                    for i in range(size):
                        if row + i >= map_size or player_board[row + i][col] != "_":
                            valid = False
                if valid:
                    ship_positions = []
                    if orientation == "H":
                        for i in range(size):
                            player_board[row][col + i] = "S"
                            ship_positions.append((row, col + i))
                    else:
                        for i in range(size):
                            player_board[row + i][col] = "S"
                            ship_positions.append((row + i, col))
                    player_ships.append((name, size, ship_positions))
                    print("  " + " ".join(str(i + 1) for i in range(len(player_board[0]))))
                    for i, row in enumerate(player_board):
                        print(row_labels[i] + " " + " ".join(row))
                    break
                else:
                    print("Invalid coordinates or orientation. Please enter correct values.")
        except ValueError:
            print("Invalid input. Please enter a valid row letter and column number.")

# computer ship placement
for size, name in zip(ship_sizes, ship_names):
    while True:
        row = randrange(0, map_size)
        col = randrange(0, map_size)
        orientation = "H" if randrange(2) == 0 else "V"
        valid = True
        if orientation == "H":
            if col + size > map_size:
                valid = False
            for i in range(size):
                if col + i >= map_size or comp_board[row][col + i] != "_":
                    valid = False
        else:
            if row + size > map_size:
                valid = False
            for i in range(size):
                if row + i >= map_size or comp_board[row + i][col] != "_":
                    valid = False
        if valid:
            ship_positions = []
            if orientation == "H":
                for i in range(size):
                    comp_board[row][col + i] = "S"
                    ship_positions.append((row, col + i))
            else:
                for i in range(size):
                    comp_board[row + i][col] = "S"
                    ship_positions.append((row + i, col))
            comp_ships.append((name, size, ship_positions))
            break
# AI
# initialize target mode variables
target_mode = False
target_hits = []
direction_mode = False
direction = (0, 0)
directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # right, left, up, down

# main game loop
player_hits = 0
comp_hits = 0
while True:
    # player's turn
    try:
        row = row_labels.index(input("Enter your row (A-J): ").upper())
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
            print("You have already attacked this position. Please select another position.")
            continue
        else:
            comp_board[row][col] = "*"
            dummy_board[row][col] = "*"
            print("Missed!")
            playsound('ship-miss.mp3')
    except ValueError:
        print("Invalid input. Please enter a valid row letter and column number.")
        continue

    if player_hits == sum(ship_sizes):
        print("All ships have been sunk!")
        print("Player has won - game over")
        playsound('win.wav')
        break

    # computer's turn
    while True:
        if target_mode:
            if direction_mode:
                last_hit = target_hits[-1]
                row, col = last_hit[0] + direction[0], last_hit[1] + direction[1]
                if not (0 <= row < map_size and 0 <= col < map_size) or player_board[row][col] in ["*", "X"]:
                    direction_mode = False
                    continue
            else:
                for d in directions:
                    row, col = target_hits[0][0] + d[0], target_hits[0][1] + d[1]
                    if 0 <= row < map_size and 0 <= col < map_size and player_board[row][col] not in ["*", "X"]:
                        direction = d
                        direction_mode = True
                        break
                if not direction_mode:
                    target_mode = False
                    target_hits = []
                    continue
        else:
            row = randrange(0, map_size)
            col = randrange(0, map_size)
            if player_board[row][col] in ["*", "X"]:
                continue

        print("Computer has selected coordinates", row_labels[row], col + 1)
        if player_board[row][col] == "S":
            player_board[row][col] = "X"
            print("Player: Ship has been hit!")
            target_mode = True
            target_hits.append((row, col))
            ship_sunk = False
            for name, size, positions in player_ships:
                if all(player_board[r][c] == "X" for r, c in positions):
                    if name not in player_sunk_ships:
                        player_sunk_ships.append(name)
                        print(f"Player: {name} (size {size}) has been sunk!")
                        playsound('ship-hit-and-sunk.mp3')
                        print(f"Player's sunk ships: {', '.join(player_sunk_ships)}")
                        ship_sunk = True
                        target_mode = False
                        direction_mode = False
                        target_hits = []
                        break
            if not ship_sunk:
                playsound('ship-hit.mp3')
        else:
            player_board[row][col] = "*"
            print("Missed!")
            playsound('ship-miss.mp3')
            if direction_mode:
                direction_mode = False
        break

    if comp_hits == sum(ship_sizes):
        print("Computer has won - game over")
        playsound('loss.wav')
        break

    print(f"Player {user_name} board")
    print("  " + " ".join(str(i + 1) for i in range(len(player_board[0]))))
    for i, row in enumerate(player_board):
        print(row_labels[i] + " " + " ".join(row))
    print(" ")
    print("Computer board")
    print("  " + " ".join(str(i + 1) for i in range(len(dummy_board[0]))))
    for i, row in enumerate(dummy_board):
        print(row_labels[i] + " " + " ".join(row))
