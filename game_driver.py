import random
import pickle
from game_functions import start_page, ending_page, new_game, load_game, save_game, monster_encounter, key_encounter, exit_check, class_check, path_decay, update_path, monster_movement
from game_elements import *


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

SCENT_PATH = []

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
    class_check(player, monster, exit_key)
    
    # TODO: add in monster movement
    # TODO: input verification for player movement
  
    #game loop
    while True:
        #
        # once a player starts in a room, they are first given a description of the room
        # if the player moves into a room with a monster, then they are first given a description of the monster and a chance to avoid
        # if the player moves into a room with a key, then they are first given a description of the key and a chance to pick it up
        # the player escapes when they reach the exit room with the key in their inventory
        #
        # TODO: clean up code, add typing, add doctrings to all functions
  
        path_decay(SCENT_PATH, ROOMS)
        player.drop_scent()
        update_path(SCENT_PATH, player.get_player_position())
        for room in SCENT_PATH:
            print(f"{room} has a scent of: {ROOMS[room].get_scent()}")

        if player.get_player_position() == monster.get_monster_position():
            if monster_encounter(player, monster):
                continue
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
            exit()

        
        player.set_position(player.position.connected_rooms[player_choice])
        monster_movement(monster, ROOMS)
        


                # player can encounter monster
                # player can escape
                # player can die
ending_page(player)
