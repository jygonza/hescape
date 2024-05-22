import random
import pickle
from game_elements import *
from utils import input_validation

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
    player = Player(input("Enter your name: "), "You are the player")
    player.set_position(room_list["Room 1"]) # player is placed in the starting room   

    monster = Monster("Monster", "A scary monster") 
    monster.set_position(random.choice(list(room_list.values())[1:])) # monster is placed in a random room that is not the starting room
    
    key = Key("Key", "A key to unlock the exit")
    key.set_position(random.choice(list(room_list.values())[1:])) # key is placed in a random room that is not the starting room
    print (key.get_key_position())
    return player, monster, key, room_list

def save_game(room_list, player, monster, key):
    # we will save the current game in the GameState object
    print("saving game...")
    game_object = GameState(room_list, player, monster, key)
    # save the game object to a pickle file
    with open("game_state.pkl", "wb") as f:
        pickle.dump(game_object, f)

# TODO: add in check so we cannot load an unexisting game
def load_game(saved_game_file):
    # when player selects to load a game we will load the last saved game
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
 

