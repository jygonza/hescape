

from typing import Any


class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = {} # not used right now
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
    
    
class Monster:
    def __init__(self, name, description, position=None):
        self.name = name
        self.description = description
        self.position = None # some room
    # monsters need to be able to move through the rooms and encounter the player
    # some function to move the monster to a connected room
    def set_position(self, room):
        self.position = room

    def get_monster_position(self):
        return self.position.get_room_name()   


class Player:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.inventory = {}
        self.position = None # current room player is in

    def set_position(self, room): # must pass in room object itself?
        self.position = room

    def get_player_position(self):
        return self.position.get_room_name()
    
    def add_to_inventory(self, item):
        self.inventory[item.name] = item

    def get_inventory(self):
        return self.inventory

class Key:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.position = None

    def set_position(self, room):
        self.position = room

    def get_key_position(self):
        if self.position is not None:
            return self.position.get_room_name()
    
    
# will track our current game state so we can save this state to a file and load it later
class GameState:
    def __init__(self, room_list, player_object, monster_object, key_object):
        # need to save, the room objects, player object, monster object, and key object, as well as the current 
        # state of their attributes
        self.rooms = room_list                   # save the list of room objects
        self.player = player_object           # save the player object
        self.monster = monster_object              # save the monster object
        self.key = key_object                  # save the key object
    
    def save_game(self):
        # save the current game state to a file
        pass