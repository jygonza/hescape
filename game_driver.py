import random
import pickle
from game_functions import start_page, ending_page, new_game, load_game, save_game, monster_encounter, key_encounter, exit_check 
from game_elements import *
from utils import input_validation

# Initialize empty room objects
# need to initialize rooms with names and descriptions, these stay the same, but their connections can differ
ROOMS = {
    "Room 1": Room("Room 1", "You are in room 1"),
    "Room 2": Room("Room 2", "You are in room 2"),
    "Room 3": Room("Room 3", "You are in room 3"),
    "Room 4": Room("Room 4", "You are in room 4"),
    "Room 5": Room("Room 5", "You are in room 5"),
    "Room 6": Room("Room 6", "You are in room 6"),
    "Room 7": Room("Room 7", "You are in room 7"),
    "Room 8": Room("Room 8", "You are in room 8"),
    "Room 9": Room("Room 9", "You are in room 9"),
    "Room 10": Room("Room 10", "You are in room 10, the exit is here but the door is locked, I need a key ..."),
}

if __name__ == "__main__":
    # player introduced to game, chooses a new game or loads a previous one
    selection = start_page()
    # initialize game elements based on selection before entering game loop, or exit
    options = {
        'n': lambda: new_game(ROOMS),
        'l': lambda: load_game() or new_game(ROOMS),
        'q': lambda: exit()
    }

    player, monster, exit_key, ROOMS = options.get(selection, lambda: None)()
    # TODO: make function (class_check in utils.py) to check objects are initialized correctly
    # debugging purposes only for now
    if isinstance(player, Player):
        print("player initialized")
    else:
        print("player not initialized")
    if isinstance(monster, Monster):
        print("monster initialized")
    else:
        print("monster not initialized")
    if isinstance(exit_key, Key):  
        print("key initialized")
    else:   
        print("key not initialized")
    #game loop
    while True:
        #
        # once a player starts in a room, they are first given a description of the room
        # if the player moves into a room with a monster, then they are first given a description of the monster and a chance to avoid
        # if the player moves into a room with a key, then they are first given a description of the key and a chance to pick it up
        # the player escapes when they reach the exit room with the key in their inventory
        #
        # TODO: update saving the game, must be able to save multiple different games
            # TODO: add in check so player names must be unique from current saved games
            # TODO: add in check so we cannot load an unexisting game
            # TODO: if a game is finished, the saved_game pickle file should be deleted
                # and the player name should be removed from the player_list.json file
        # TODO: clean up code, add typing, add doctrings to all functions
        print(player.position.get_room_description())

        if player.get_player_position() == monster.get_monster_position():
            monster_encounter(player, monster)
            if player.get_status()[0] == False:
                break

        if exit_key.get_key_position() is not None and player.get_player_position() == exit_key.get_key_position():
            key_encounter(player, exit_key)

        if player.get_player_position() == "Room 10" and exit_check(player, exit_key):
            break # exit game loop
        
        print("Connected rooms:")
        for room in player.position.get_connected_rooms().keys():
            print("\t",room)
        player_choice = input("Enter the room you would like to move to or press 's' to save game: ")
        if player_choice == "s":
            save_game(player, monster, exit_key, ROOMS, player.get_player_name())
            print("Game saved")
            exit()

        player.set_position(player.position.connected_rooms[player_choice])

                # player can encounter monster
                # player can escape
                # player can die
ending_page(player)
