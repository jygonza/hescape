import random
import pickle
from game_elements import *

# create start page for the GUI
def start_page():
    print("Welcome to the game!")
    print("""
        You are stuck inside an intermediate space between dimensions, 
        you don't remember how you got here, but you must escape. However you 
        are not alone, there are monsters that lurk here. Find the exit while 
        avoiding them. Good luck!\n"""
          )
    # player can start a new game, load a saved game, or quit the game, the specific function will be called in the game driver
    return input("Press 'n' to start a new game or 'l' to load a saved game\nPress 'q' to quit the game\n")

# a new game needs to initialize the room connections, the player objects, the monster object, and the key object
def new_game(room_list):
    # when player selects to start a new game we will create a new game from scratch
    print("new game starting...")
    room_list = connect_rooms(room_list)
    player = Player(input("Enter your name: "), "You are the player")
    player.set_position(room_list[0]) # player is placed in the starting room   

    monster = Monster("Monster", "A scary monster") 
    monster.set_position(random.choice(room_list[1:])) # monster is placed in a random room that is not the starting room
    
    key = Key("Key", "A key to unlock the exit")
    key.set_position(random.choice(room_list[1:])) # key is placed in a random room that is not the starting room
    print (key.get_key_position())
    return player, monster, key, room_list

def save_game(room_list, player, monster, key):
    # we will save the current game in the GameState object
    print("saving game...")
    game_object = GameState(room_list, player, monster, key)
    # save the game object to a pickle file
    with open("game_state.pkl", "wb") as f:
        pickle.dump(game_object, f)


def load_game(saved_game_file):
    # when player selects to load a game we will load the last saved game
    print("loading game...")
    with open(saved_game_file, "rb") as f:
        game_object = pickle.load(f)
    return game_object.player, game_object.monster, game_object.key, game_object.rooms


def game_loop(player, monster, key):
    # load starting room before game loop begins
    # game loop begins
        # player enters a new room and is given a description of the room
        # if the player encounters a monster, they are given a description of the monster and a chance to avoid it
        # if the player encounters a key, they are given a description of the key and a chance to pick it up
        # if the player is in the exit room with the key in their inventory, they win
        # after all events, player is given a choice to move to a connected room to continue exploring
    # game loop ends if player dies to monster or player escapes
    pass

def ending_page(player):
    # Display end result depending on if player dies or escapes
    # if player is in the exit room with the key in their inventory, they win
    # if the player has died after encountering a monster, they lose
    print("Game over")
    
# need to alter this so that all rooms are connected into a graph
# takes in a list of rooms and connects them randomly
def connect_rooms(room_list):
    # randomly connect rooms, each room object has a connected_rooms attribute that is a dictionary using the room.name attribute as the keys
    for room in room_list:
        # connect room to at least 1 room, room cannot be connected to itself
        available_rooms = [r for r in room_list if r != room]  # Exclude the current room from the available choices
        room.connect(random.choice(available_rooms))
        # connect room to a max of 3 other rooms that is not itself
        for _ in range(random.randint(0,3)):
            room.connect(random.choice(available_rooms))


    return room_list

