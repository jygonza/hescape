import random
import pickle
from gui_driver import start_page, ending_page, new_game, load_game, save_game, monster_encounter # change this later by listing specifically the functions, alter all the imports in all the flies
from game_elements import *

# Initialize game "map" with rooms
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
        'l': lambda: load_game("game_state.pkl"),
        'q': lambda: exit()
    }
    player, monster, exit_key = options.get(selection, lambda: None)()

    #game loop
    while True:
        #
        # once a player starts in a room, they are first given a description of the room
        # if the player moves into a room with a monster, then they are first given a description of the monster and a chance to avoid
        # if the player moves into a room with a key, then they are first given a description of the key and a chance to pick it up
        # the player escapes when they reach the exit room with the key in their inventory
        #
        # TODO: change player inventory, instead each object will have a boolean attribute to check if
        #       the player has the object in their inventory

        # TODO: add input verification for all inputs
        # TODO: update saving the game, must be able to save multiple different games
        # TODO: update connect rooms function to get a valid map every time
        # TODO: rooms will track objects in their inventories, objects will track if they have been picked up 
        # TODO: clean up code, add typing, add doctrings to all functions
        print(player.position.get_room_description())

        if player.get_player_position() == monster.get_monster_position():
            monster_encounter(player, monster)


        if exit_key.get_key_position() is not None and player.get_player_position() == exit_key.get_key_position():
            print("You have found the key")
            pick = input("press 'p' to pick up the key or 'e' to leave it")
            pick = pick.lower()
            while pick not in ['p', 'e']:
                print("Invalid input. Please try again.")
                pick = input("press 'p' to pick up the key or 'e' to leave it")
            print("You have picked up the key")
            print("You can now unlock the exit")
            player.pick_up_key()
            exit_key.pick_up()
            print("The exit key is added to inventory")


        if player.get_player_position() == "Room 10":       
            if player.exit_check(): 
                print("You take the key out of your pocket and unlock the door")
                print("You have escaped the dimension")
                break
            else:
                print("The door is locked, you need a key to unlock it")


        print("Choose a room to move to or save progress by pressing 's'")
        for room in player.position.get_connected_rooms().keys():
            print(room)
        player_choice = input()
        if player_choice == "s":
            save_game(ROOMS, player, monster, exit_key)
            print("Game saved")
            exit()

        player.set_position(player.position.connected_rooms[player_choice])

                # player can encounter monster
                # player can escape
                # player can die
ending_page(player)
