import random
import pickle
from gui_driver import *
from game_elements import *

# Initialize game "map" with rooms
# need to initialize rooms with names and descriptions, these stay the same, but their connections can differ
ROOMS = [
    Room("Room 1", "You are in room 1"),
    Room("Room 2", "You are in room 2"),
    Room("Room 3", "You are in room 3"),
    Room("Room 4", "You are in room 4"),
    Room("Room 5", "You are in room 5"),
    Room("Room 6", "You are in room 6"),
    Room("Room 7", "You are in room 7"),
    Room("Room 8", "You are in room 8"),
    Room("Room 9", "You are in room 9"),
    Room("Room 10", "You are in room 10, the exit is here but the door is locked, I need a key ..."),
    ]

# rooms must be connected to at least 1 room and can be connected to a max of 3 other rooms that is not itself


if __name__ == "__main__":

    # player introduced to game, chooses a new game or loads a previous one
    selection = start_page()
    if selection == 'n':
        # start new game
        player, monster, exit_key, ROOMS = new_game(ROOMS)
    elif selection == 'l':
        # load saved game
        player, monster, exit_key, ROOMS = load_game("game_state.pkl")
    elif selection == 'q':
        # quit game
        print("Goodbye!")
        exit()

    # initialize game elements based on selection before entering game loop, or exit

    #game loop
    while True:
        #
        # once a player starts in a room, they are first given a description of the room
        # if the player moves into a room with a monster, then they are first given a description of the monster and a chance to avoid
        # if the player moves into a room with a key, then they are first given a description of the key and a chance to pick it up
        # the player escapes when they reach the exit room with the key in their inventory
        print(player.position.get_room_description())

        if player.get_player_position() == monster.get_monster_position():
            print("You encounter a monster")
            print(monster.description)
            # player will now haRve options for interaction: player must choose correct way to avoid the monster
            press = input("Press 'e' to escape or 's' to stay still")
            if press == 'e':
                # run to randomly connected room to escape
                #escape_to = list(player.position.get_connected_rooms().keys())# list of keys
                #player.set_position(player.position.connected_rooms[random.choice(escape_to)]) # use key to index room object
                print("You have escaped the monster")


            elif press == 's':
                print("You have been eaten by the monster")
                break
        

        if exit_key.get_key_position is not None and player.get_player_position() == exit_key.get_key_position():
            print("You have found the key")
            pick = input("press 'p' to pick up the key")
            if pick == 'p':
                print("You have picked up the key")
                print("You can now unlock the exit")
                player.add_to_inventory(exit_key)
                print(f"{exit_key} added to inventory: {player.get_inventory()}")
                # remove key from room
                exit_key.set_position(None)

        if player.get_player_position == ROOMS[9].get_room_name(): # this check is not working
            if exit_key in player.get_inventory():
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
