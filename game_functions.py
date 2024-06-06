import random
import pickle
from game_elements import *
from utils import input_validation, show_saved_games, update_player_list, is_name_unique, player_name_check, open_file, delete_saved_game, is_new_game

# create start page for the GUI
def start_page():
    print("Welcome to the game!")
    print("""
        You are stuck inside an intermediate space between dimensions, 
        you don't remember how you got here, but you must escape. However you 
        are not alone, there are monsters that lurk here. Find the exit while 
        avoiding them. Good luck!\n"""
          )
    print("Press 'n' to start a new game or 'l' to load a saved game\nPress 'q' to quit the game")
    return input_validation(input("Enter your selection: "), ['n', 'l', 'q'])

# a new game needs to initialize the room connections, the player objects, the monster object, and the key object
def new_game(room_list):
    print("new game starting...")
    connect_rooms2(room_list)
    # TODO: player name must not be currently attached to an existing game
    player_list = open_file("player_list.json") or []
    player_name = player_name_check(input("Enter your player name: "), player_list)

    player = Player(player_name, "You are the player") # player object is created
    player.set_position(room_list["Room 1"]) # player is placed in the starting room   

    monster = Monster("Monster", "A scary monster") 
    monster.set_position(random.choice(list(room_list.values())[1:])) # monster is placed in a random room that is not the starting room
    
    key = Key("Key", "A key to unlock the exit")
    key.set_position(random.choice(list(room_list.values())[1:])) # key is placed in a random room that is not the starting room

    return player, monster, key, room_list

def save_game(player, monster, key, room_list, player_id): # player_id will be player.name
    player_list = open_file("player_list.json") or []
    if is_name_unique(player_id, player_list):
        try:
            if update_player_list(player_id):
                print("saving player list...")
                game_state = GameState(player, monster, key, room_list)
                with open(f"game_save_{player_id}.pkl", "wb") as f:
                    pickle.dump(game_state, f)
                    print("Game saved")
            else:
                print("Could not save player list, too many saved games")
        except Exception as e:
            print(e)
    elif not is_name_unique(player_id, open_file("player_list.json")):
        game_state = GameState(player, monster, key, room_list)
        with open(f"game_save_{player_id}.pkl", "wb") as f:
            pickle.dump(game_state, f)
            print("Game saved")
    else:
        print("Could not save game")
        return False


# if a player enters in a wrong name, they can try again, or choose a new game
# if no saved games, return False, game_driver will instead call for new_game
def load_game():
    check, player_list = show_saved_games()
    if not check:
        return False
    player_id = input("Enter the player name to load the game: ")
    while player_id not in player_list:
        print("Player name not found")
        player_id = input("Enter the player name to load the game or press 'n' for a new game:")
        if player_id == 'n':
            return False
    saved_game_file = f"game_save_{player_id}.pkl"

    print("loading game...")
    with open(saved_game_file, "rb") as f:
        game_object = pickle.load(f)
    return game_object.player, game_object.monster, game_object.key, game_object.rooms
    

# TODO: implement reset game function
#def reset_game(room_list):
    ##for room in room_list.values():
        #room.reset_room()

def monster_encounter(player, monster):
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
        player.player_hit()
        return False
    
def key_encounter(player, key):
    # if player encounters a key, they are given a description of the key and a chance to pick it up
    print("You have found a key")
    print(key.description)
    # player will now have options for interaction: player must choose correct way to pick up the key
    pick = input_validation(input("Press 'p' to pick up the key or 'l' to leave it: "), ['p', 'l'])
    if pick == 'p':
        key.pick_up()
        print("You have picked up the key")
    else:
        print("You have left the key")
    
def exit_check(player, key):
    # check if key has been picked up
    if key.key_check() == True:
        print("You take the key out of your pocket and unlock the door")
        player.player_escape()
        return True
    else:
        print("The door is locked, you need a key to unlock it")
        return False

def ending_page(player):
    # Display end result depending on if player dies or escapes
    # if player is in the exit room with the key in their inventory, they win
    # if the player has died after encountering a monster, they lose
    if player.get_status()[0] == True and player.get_status()[1] == True:
        print("You have escaped the dimension, you win!")
    elif player.get_status()[0] == False:
        print("You have been eaten by a monster, you lose!")
    print("Game over")
    delete_saved_game(player.get_player_name())
    choice = input_validation(input("Press 'q' to quit the game"), ['q'])
    if choice == 'q':
        exit()
    

# takes in a dict of rooms and connects them randomly
def connect_rooms(room_list):
    # randomly connect rooms, each room object has a connected_rooms attribute that is a dictionary using the room.name attribute as the keys
    for room in room_list.values():
        available_rooms = [r for r in room_list.values() if r != room]
        for _ in range(3):
            if available_rooms:
                connected_room = random.choice(available_rooms)
                room.connect(connected_room)
                connected_room.connect(room)
    return room_list

def connect_rooms2(room_list):
    # randomly connect rooms, each room object has a connected_rooms attribute that is a dictionary using the room.name attribute as the keys
    decay_list = list(room_list.values())
    for room in list(room_list.values()):
        # connect room to at least 1 room, room cannot be connected to itself   
        available_rooms = [r for r in decay_list if r != room and len(r.get_connected_rooms()) < 4]
        # connect room to a max of 3 other rooms that is not itself
   
        for _ in range(3):
            if available_rooms and len(room.get_connected_rooms()) < 4:
                connected_room = random.choice(available_rooms)
                room.connect(connected_room)
                connected_room.connect(room)
                if len(connected_room.get_connected_rooms()) >= 4 and connected_room in decay_list:
                    decay_list.remove(connected_room)
                if len(room.get_connected_rooms()) >= 4 and room in decay_list:
                    decay_list.remove(room)
    return room_list
 
def class_check(player, monster, key):
    """
    Checks if instances of Player, Monster, and Key classes are initialized and prints corresponding messages.

    Args:
        player: An instance to check if it's of the Player class.
        monster: An instance to check if it's of the Monster class.
        key: An instance to check if it's of the Key class.

    Returns:
        tuple: A tuple containing the player, monster, and key instances.
    """

    try:
        assert isinstance(player, Player)
        assert isinstance(monster, Monster)
        assert isinstance(key, Key)
        return True
    except AssertionError:
        return False

