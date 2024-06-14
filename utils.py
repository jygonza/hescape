import json
import os

def input_validation(some_input, valid_selections):
    """
    Validates user input against a set of valid selections until a valid input is provided.

    Args:some_input (str): The user input to validate.
         valid_selections (list): A list of valid selections to compare the input against.

    Returns:
        str: The validated user input.
    """
    valid_selections_set = set(valid_selections)
    while some_input.lower() not in valid_selections_set:
        some_input = input("Invalid selection. Please try again:").lower()
    return some_input


def is_name_unique(player_name, player_list):
    """
    Checks if a player name is unique among a list of player names.

    Args:
        player_name (str): The player name to check.
        player_list (list): A list of player names to compare against.

    Returns:
        bool: True if the player name is unique, False otherwise.
    """
    normalized_name = player_name.lower()
    return all(normalized_name != name.lower() for name in list(player_list))


def player_name_check(player_name, player_list):
    """
    Validates the player name to ensure it meets specified criteria.

    Args:
        player_name (str): The player's chosen name.
        player_list (list): List of existing player names.

    Returns:
        str: The validated player name.
    """

    # character limit on player name and no whitespace
    while True:
        if len(player_name) > 20 or " " in player_name:
            print("Player name must be less than 20 characters and contain no whitespace")
            player_name = input("Enter your player name: ")
        elif player_name == "":
            print("Player name cannot be empty")
            player_name = input("Enter your player name: ")
        elif not is_name_unique(player_name, player_list):
            print("Player name already exists")
            player_name = input("Enter your player name: ")
        else:
            break
    
    return player_name

def open_file(file_name): 
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def show_saved_games():
    """
    Summarizes saved games and displays them. If no saved games are found, an empty list is returned.

    Returns:
        tuple: A tuple containing a boolean indicating if saved games were found and a list of saved games.

    Raises:
        FileNotFoundError: If no saved games file is found.
    """
    try:
        with open("player_list.json", "r") as f:
            player_list = json.load(f)
        print("Saved games:")
        for i in range(0, len(player_list), 2):
            print(f"{player_list[i]:<20} {player_list[i+1] if i+1 < len(player_list) else ''}")
        return True, player_list
    except FileNotFoundError:
        print("No saved games found")
        player_list = []
        return False, player_list
    
def is_new_game(player_name, player_list): # am I using this function?
    """
    Check if the player name is new or already exists in the player list.

    Args:
        player_name (str): The player name to check.
        player_list (list): A list of player names to compare against.

    Returns:
        bool: True if the player name is new, False otherwise.
    """
    return player_name not in player_list


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



def delete_saved_game(player_id):
    """
    Delete a saved game file and remove the player ID from the player list.
    If the saved game file exists, it is deleted. If the player list file exists, the player ID is removed from the list. If the player list file does not exist, no action is taken.
    
    Args:
        player_id (str): The player ID to be removed from the player list.
    """

    saved_game_file = f"game_save_{player_id}.pkl"
    if os.path.exists(saved_game_file):
        os.remove(saved_game_file)

    if os.path.exists("player_list.json"):
        with open("player_list.json", "r+") as f:
            player_list = json.load(f)
            if player_id in player_list:
                player_list.remove(player_id)
                f.seek(0)
                json.dump(player_list, f)
                f.truncate()
