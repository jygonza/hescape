import json
def open_file(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


player_list = open_file("player_list.json")



player_list = open_file("player_list.json")
print(player_list) # None
player_name = "thor"

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


    for name in player_list:
        if normalized_name == name.lower(): # this is failing beacuse
            return False
    return True

print(is_name_unique(player_name, player_list)) # True

for name in list(player_list):
    print(name.lower())


print(type(player_list))
print(player_list[0])