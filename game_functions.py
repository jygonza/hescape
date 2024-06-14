import random
import pickle
from game_elements import *
from utils import input_validation, show_saved_games, update_player_list, is_name_unique, player_name_check, open_file, delete_saved_game, is_new_game

def start_page():
    """
    Displays the welcome message and options to start, load, or quit the game.

    Returns:
        str: The user's selection after input validation.
    """

    print("Welcome to the game!")
    print("""
        You are stuck inside an intermediate space between dimensions, 
        you don't remember how you got here, but you must escape. However you 
        are not alone, there are monsters that lurk here. Find the exit while 
        avoiding them. Good luck!\n"""
          )
    print("Press 'n' to start a new game or 'l' to load a saved game\nPress 'q' to quit the game")
    return input_validation(input("Enter your selection: "), ['n', 'l', 'q'])


def new_game(room_dict):
    """
    Start a new game by initializing player, monster, key, and room placements.
    Prints a message indicating the start of a new game, connects rooms, prompts the player to enter their name, creates player, monster, and key objects, places them in random rooms, and returns player, monster, key, and room_list.

    Args:
        room_list: A dictionary containing room objects for the game.

    Returns:
        Tuple containing player, monster, key, and room_list objects.
    """

    print("new game starting...")
    connect_rooms(room_dict)
    player_list = open_file("player_list.json") or []
    player_name = player_name_check(input("Enter your player name: "), player_list) # player name is checked for uniqueness and length, function in utils.py

    player = Player(player_name, "You are the player") 
    player.set_position(room_dict["Room 1"]) # player is placed in the starting room 1  

    monster = Monster("Monster", "A scary monster") 
    monster.set_position(random.choice(list(room_dict.values())[1:])) # monster is placed in a random room that is not the starting room
    
    key = Key("Key", "A key to unlock the exit")
    key.set_position(random.choice(list(room_dict.values())[1:])) # key is placed in a random room that is not the starting room

    return player, monster, key, room_dict

def save_game(player, monster, key, room_dict, player_id): # player_id will be player.name
    """
    Saves the current game state with the player, monster, key, and room list.

    Args:
        player: The player object.
        monster: The monster object.
        key: The key object.
        room_list: List of room objects.
        player_id (str): The unique identifier for the player. (player.name)

    Returns:
        bool: True if the game is saved successfully, False otherwise.
    """

    player_list = open_file("player_list.json") or []
    if is_name_unique(player_id, player_list): # if the player has never saved a game, then we will add them to the player list and save the game
        try:
            if update_player_list(player_id): # returns False if player was not added (either list is full or an error occurred)
                print("saving player list...")
                game_state = GameState(player, monster, key, room_dict)
                with open(f"game_save_{player_id}.pkl", "wb") as f:
                    pickle.dump(game_state, f)
                    print("Game saved")
            else:
                print("Could not save player list, too many saved games")
        except Exception as e: 
            print(e)

    elif not is_name_unique(player_id, open_file("player_list.json")): # if the player has saved a game before, then we will overwrite the saved game
        game_state = GameState(player, monster, key, room_dict)
        with open(f"game_save_{player_id}.pkl", "wb") as f:
            pickle.dump(game_state, f)
            print("Game saved")
    else:
        print("Could not save game")
        return False


def load_game():
    """
    Loads a saved game based on the player's input.

    Returns:
        tuple: The player object, monster object, key object, and room list from the saved game.
    """

    check, player_list = show_saved_games() # returns a tuple of a boolean and a either an empty list or a list of player names
    if not check: # if there are no saved games, then the player will start a new game
        return False
    player_id = input("Enter the player name to load the game: ")
    while player_id not in player_list: # player must enter a valid player name
        print("Player name not found")
        player_id = input("Enter the player name to load the game or press 'n' for a new game:")
        if player_id == 'n': # player can choose to start a new game if they don't have a saved game
            return False
    saved_game_file = f"game_save_{player_id}.pkl" # game save files are named with the player name

    print("loading game...")
    with open(saved_game_file, "rb") as f: 
        game_object = pickle.load(f)
    return game_object.player, game_object.monster, game_object.key, game_object.rooms
    

# TODO: implement reset game function for after a player wins or loses
#def reset_game(room_list):
    ##for room in room_list.values():
        #room.reset_room()

def monster_encounter(player, monster):
    """
    Handles the encounter between the player and a monster once they are in the same room.

    Args:
        player: The player object.
        monster: The monster object.

    Returns:
        bool: True if the player successfully escapes, False if the player gets caught by the monster.
    """

    # if player encounters a monster, they are given a description of the monster and a chance to avoid it
    print("You encounter a monster")
    print(monster.description)
    # player will now have options for interaction: player must choose correct way to avoid the monster
    press = input_validation(input("Press 'e' to escape or 's' to stay still: "), ['e', 's'])
    if press == 'e':
        # run to randomly connected room to escape
        escape_to = list(player.position.get_connected_rooms().keys())  # list of keys
        escape_room = random.choice(escape_to)
        player.set_position(player.position.connected_rooms[escape_room])  # use key to index room object
        print("You have escaped the monster and ran to ", player.get_player_position())
        return True
    elif press == 's':
        print("Frozen in fear, you are unable to make the right choice and the monster eats you")
        player.player_hit() # player_hit sets player.alive to False
        return False

def key_encounter(player, key):
    """
    Handles the encounter between the player and a key.

    Args:
        player: The player object.
        key: The key object.

    Returns:
        None
    """
    # if player encounters a key, they are given a description of the key and a chance to pick it up
    print("You have found a key")
    print(key.description)
    pick = input_validation(input("Press 'p' to pick up the key or 'l' to leave it: "), ['p', 'l'])
    if pick == 'p':
        key.pick_up()
        print("You have picked up the key")
    else:
        print("You have left the key")
    
def exit_check(player, key):
    """
    Checks if the player has picked up the key to unlock the door.

    Args:
        player: The player object.
        key: The key object.

    Returns:
        bool: True if the key is picked up, False otherwise.
    """
    if key.key_check() == True:
        print("You take the key out of your pocket and unlock the door")
        player.player_escape() # sets player.escaped to True for the ending check
        return True
    else:
        print("The door is locked, you need a key to unlock it")
        return False

def ending_page(player):
    """
    Displays the end result of the game based on the player's status, deletes the saved game, and prompts the player to quit the game.

    Args:
        player: The player object.

    Returns:
        None
    """

    if player.get_status()[0] == True and player.get_status()[1] == True:
        print("You have escaped the dimension, you win!")
    elif player.get_status()[0] == False:
        print("You have been eaten by a monster, you lose!")
    print("Game over")
    delete_saved_game(player.get_player_name())
    choice = input_validation(input("Press 'q' to quit the game"), ['q'])
    if choice == 'q':
        exit()
    

def connect_rooms(room_dict):
    """
    Randomly connects rooms in the game.

    Args:
        room_dict (dict): A dictionary of room objects.

    Returns:
        dict: The updated room dictionary with connected rooms.
    """

    # randomly connect rooms, each room object has a connected_rooms attribute that is a dictionary using the room.name attribute as the keys
    decay_list = list(room_dict.values())
    for room in list(room_dict.values()):
        available_rooms = [r for r in decay_list if r != room and len(r.get_connected_rooms()) < 4]

        for _ in range(3):
            if available_rooms and len(room.get_connected_rooms()) < 4:
                connected_room = random.choice(available_rooms)
                room.connect(connected_room)
                connected_room.connect(room)
                if len(connected_room.get_connected_rooms()) >= 4 and connected_room in decay_list:
                    decay_list.remove(connected_room)
                if len(room.get_connected_rooms()) >= 4 and room in decay_list:
                    decay_list.remove(room)
    return room_dict
 
def class_check(player, monster, key):
    """
    Checks if instances of Player, Monster, and Key classes are initialized and prints corresponding messages.

    Args:
        player: An instance to check if it's of the Player class.
        monster: An instance to check if it's of the Monster class.
        key: An instance to check if it's of the Key class.

    Returns:
        bool: True if all instances are of the correct class, False otherwise.
    """

    try:
        assert isinstance(player, Player)
        assert isinstance(monster, Monster)
        assert isinstance(key, Key)
        return True
    except AssertionError:
        return False

def update_path(scent_path, room):
    if room not in scent_path:
        scent_path.append(room)
        #print(f"{room} added to path")

def path_decay(scent_path, room_dict):
    """
    Decay the scent path by dissipating scent in each room and removing rooms with zero or negative scent levels.

    Args:
        scent_path: List of rooms representing the scent path.
        room_dict: Dictionary mapping room names to Room objects.

    Returns:
        None
    """
    rooms_to_remove = []

    for room in scent_path:
        room_dict[room].dissipate_scent()
        if room_dict[room].get_scent() <= 0:
            rooms_to_remove.append(room)
    for room in rooms_to_remove:
        scent_path.remove(room)


def monster_movement(monster,room_dict):
    """
    Moves the monster. If the monster is nearby the scent path it will follow it, otherwise it will move to a random connected room.

    Args:
        monster: The monster object.
        room_list (list): List of room objects.

    Returns:
        None
    """
    max_scent = 0
    # get connected rooms returns a dict 
    connections = room_dict[monster.get_monster_position()].get_connected_rooms().values()
    for room in connections:
        if room.get_scent() > max_scent:
            max_scent = room.get_scent()
            next_room = room
    if max_scent == 0:
        next_room = random.choice(list(connections))
    monster.set_position(next_room)
    print(f"The monster has moved to {monster.get_monster_position()}")# only for debugging purposes