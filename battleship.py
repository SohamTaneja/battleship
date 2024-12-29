from random import randrange
from playsound import playsound

ship_sizes = [5, 4, 3, 3, 2]
ship_names = ["Carrier", "Battleship", "Cruiser", "Submarine", "Destroyer"]
map_size = 10  # Map size changed to 10x10
row_labels = "ABCDEFGHIJ"  # Row labels A-J

# Get username
while True:
    user_name = input("Enter your name: ")
    if user_name:
        print(f"Welcome to the battleship game {user_name}!")
        break
    else:
        print("Please enter your name.")

# Create battlefield
player_board = [["_"] * map_size for _ in range(map_size)]
comp_board = [["_"] * map_size for _ in range(map_size)]
dummy_board = [["_"] * map_size for _ in range(map_size)]

# Track ship positions
player_ships = []
comp_ships = []

# Track sunk ships
player_sunk_ships = []
comp_sunk_ships = []

# Display battlefield
print("  " + " ".join(str(i + 1) for i in range(len(player_board[0]))))  # Display 1-10 for columns
for i, row in enumerate(player_board):
    print(row_labels[i] + " " + " ".join(row))  # Display A-J for rows

# Place ships for player
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
                    # Display the board after placing the ship
                    print("  " + " ".join(str(i + 1) for i in range(len(player_board[0]))))  # Display 1-10 for columns
                    for i, row in enumerate(player_board):
                        print(row_labels[i] + " " + " ".join(row))  # Display A-J for rows
                    break
                else:
                    print("Invalid coordinates or orientation. Please enter correct values.")
        except ValueError:
            print("Invalid input. Please enter a valid row letter and column number.")

# Place ships for computer
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

# Game loop
player_hits = 0
comp_hits = 0
while True:
    # Player's turn
    print(user_name)
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
                        playsound('C:/Users/soham/Downloads/ship-hit-and-sunk.mp3')  # Play sink sound
                        print(f"Computer's sunk ships: {', '.join(comp_sunk_ships)}")
                        ship_sunk = True
                        break
            if not ship_sunk:
                playsound('C:/Users/soham/Downloads/ship-hit.mp3')  # Play hit sound
            player_hits += 1
        else:
            dummy_board[row][col] = "*"
            print("Missed!")
            playsound('C:/Users/soham/Downloads/ship-miss.mp3')  # Play miss sound
    except ValueError:
        print("Invalid input. Please enter a valid row letter and column number.")
        continue
    
    if player_hits == sum(ship_sizes):
        print("Player has won - game over")
        break

    # Computer's turn
    while True:
        row = randrange(0, map_size)
        col = randrange(0, map_size)
        if player_board[row][col] not in ["*", "X"]:
            break
    print("Computer has selected coordinates", row_labels[row], col + 1)
    if player_board[row][col] == "S":
        player_board[row][col] = "X"
        print("Player: Ship has been hit!")
        ship_sunk = False
        for name, size, positions in player_ships:
            if all(player_board[r][c] == "X" for r, c in positions):
                if name not in player_sunk_ships:
                    player_sunk_ships.append(name)
                    print(f"Player: {name} (size {size}) has been sunk!")
                    playsound('C:/Users/soham/Downloads/ship-hit-and-sunk.mp3')  # Play sink sound
                    print(f"Player's sunk ships: {', '.join(player_sunk_ships)}")
                    ship_sunk = True
                    break
        if not ship_sunk:
            playsound('C:/Users/soham/Downloads/ship-hit.mp3')  # Play hit sound
        comp_hits += 1
    else:
        player_board[row][col] = "*"
        print("Missed!")
        playsound('C:/Users/soham/Downloads/ship-miss.mp3')  # Play miss sound
    
    if comp_hits == sum(ship_sizes):
        print("Computer has won - game over")
        break

    print(f"Player {user_name} board")
    print("  " + " ".join(str(i + 1) for i in range(len(player_board[0]))))  # Display 1-10 for columns
    for i, row in enumerate(player_board):
        print(row_labels[i] + " " + " ".join(row))  # Display A-J for rows
    print(" ")
    print("Computer board")
    print("  " + " ".join(str(i + 1) for i in range(len(dummy_board[0]))))  # Display 1-10 for columns
    for i, row in enumerate(dummy_board):
        print(row_labels[i] + " " + " ".join(row))  # Display A-J for rows
