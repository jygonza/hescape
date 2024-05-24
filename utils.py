import json
import os

def input_validation(some_input, valid_selections):
    valid_selections_set = set(valid_selections)
    while some_input.lower() not in valid_selections_set:
        some_input = input("Invalid selection. Please try again:").lower()
    return some_input

# TODO: still needs work 
def player_name_check(player_name, player_list):
    while player_name.lower() in player_list:
        player_name = input("Player name already exists, please enter a new name: ").lower()
    return player_name

def show_saved_games():
    try:
        with open("player_list.json", "r") as f:
            player_list = json.load(f)
        print("Saved games:")
        for i in range(0, len(player_list), 2):
            print(f"{player_list[i]:<20} {player_list[i+1] if i+1 < len(player_list) else ''}")
        return True
    except FileNotFoundError:
        print("No saved games found")
        return False

def update_player_list(player_id):
    """
    Update the player list with a new player ID if the list is not full.

    If the player list file exists and has fewer than 10 entries, the player ID is added to the list. If the list is full, no update is made. If the file does not exist, a new file is created with the player ID.
    Args:
        player_id (str): The player ID to be added to the player list.
    Returns:
        bool: True if the player ID was successfully added to the list, False otherwise.
    """

    if os.path.exists("player_list.json"):
        with open("player_list.json", "r+") as f:
            player_list = json.load(f)
            if len(player_list) < 10:
                player_list.append(player_id)
                f.seek(0)
                json.dump(player_list, f)
                f.truncate()
                return True
    else:
       with open("player_list.json", "w") as f:
           json.dump([player_id], f)
           return True
    return False

# TODO: needs to be implemented, ensures we are loading and saving game objects
#       to the correct variables
def class_check(player, monster, key):
    pass