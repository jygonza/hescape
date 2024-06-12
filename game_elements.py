

from typing import Any

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        # scent will be used to track the player's path through the game
        self.scent = 0
        #self.items = {} # not used right now
        self.connected_rooms = {}


    # only connecting rooms when intializing all game elements
    def connect(self, room):
        self.connected_rooms[room.name] = room

    # when the player moves we will get all the connected rooms that the player can move to
    def get_connected_rooms(self):
        return self.connected_rooms
    
    def get_room_description(self):
        return self.description
    
    def get_room_name(self):
        return self.name
    
    # a scent will naturally decay over time
    def dissipate_scent(self):
        self.scent -= 1
    
    def get_scent(self):    
        return self.scent

    def reset_room(self):
        self.connected_rooms = {}
        
# TODO: add monster movement
class Monster:
    def __init__(self, name, description, position=None):
        self.name = name
        self.description = description
        self.position = None # some room

    def set_position(self, room): # position is a room object
        self.position = room

    def get_monster_position(self):
        return self.position.get_room_name()   


class Player:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.position = None 
        self.alive = True
        self.escaped = False
        #self.has_key = False

    def set_position(self, room): # position is a room object
        self.position = room

    def get_player_position(self): # returns the name of the room the player is in
        return self.position.get_room_name()
    
    def get_player_name(self):
        return self.name

    def get_status(self):
        return self.alive, self.escaped
    
    def player_hit(self):
        self.alive = False

    def player_escape(self):
        self.escaped = True
    
    def drop_scent(self):
        self.position.scent += 3


class Key:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.position = None
        self.picked_up = False

    def set_position(self, room):
        self.position = room

    def get_key_position(self):
        if self.position is not None:
            return self.position.get_room_name()
        
    def pick_up(self):
        self.picked_up = True
        self.position = None
    
    def key_check(self):
        return self.picked_up
# will track our current game state so we can save this state to a file and load it later
class GameState:
    def __init__(self, player_object, monster_object, key_object, room_list):
        # need to save, the room objects, player object, monster object, and key object, as well as the current 
        # state of their attributes
        self.rooms = room_list                   # save the list of room objects
        self.player = player_object           # save the player object
        self.monster = monster_object              # save the monster object
        self.key = key_object                  # save the key object
    
    def save_game(self):
        # save the current game state to a file
        pass

class StartPage:
    def __init__(self):
        self.selection = None
        self.options = {
            # 'n': lambda: new_game(ROOMS),
            # 'l': lambda: load_game() or new_game(ROOMS),
            # 'q': lambda: exit()
        }
    def start_text(self):
        pass
    def new_game(self, ROOMS):
        pass
    def load_game(self):
        pass
    def exit(self):
        pass

# TODO: overlaps with GameState? can we combine these two classes?
class GameScreen:
    def __init__(self, player, monster, exit_key, rooms):
        self.player = player
        self.monster = monster
        self.exit_key = exit_key
        self.rooms = rooms

    def display_player_position(self):
        print(self.player.get_player_position())

    def display_room_description(self):
        print(self.player.position.get_room_description())

    def display_connected_rooms(self):
        for room in self.player.position.get_connected_rooms().keys():
            print("\t",room)

    def handle_encounter(self):
        pass

    