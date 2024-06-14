from typing import Any

class Room:
    """
    Represents a room in the game.

    Args:
        name (str): The name of the room.
        description (str): The description of the room.

    Methods:
        connect(room): Takes a room object as argument and adds it to our connected rooms dictionary.
        get_connected_rooms(): Returns our dictionary of connected rooms.
        get_room_description(): Returns the description of the room.
        get_room_name(): Returns the name of the room.
        dissipate_scent(): Decreases the scent of the room by 1.
        get_scent(): Returns the current scent of the room.
        reset_room(): Resets the connected rooms of the room.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.scent = 0
        self.connected_rooms = {}

    # connect is called in the connect_rooms function in game_functions.py
    def connect(self, room): # room is a room object, it's name attribute will be used as its key in the dictionary
        self.connected_rooms[room.name] = room

    def get_connected_rooms(self):
        return self.connected_rooms
    
    def get_room_description(self):
        return self.description
    
    def get_room_name(self):
        return self.name
    
    def dissipate_scent(self):
        self.scent -= 1
    
    def get_scent(self):    
        return self.scent

    def reset_room(self):
        self.connected_rooms = {}
        
class Monster:
    """
    Represents a monster in the game.

    Args:
        name (str): The name of the monster.
        description (str): The description of the monster.
        position: The room where the monster is located.

    Methods:
        set_position(room): Sets the position of the monster to a specific room.
        get_monster_position(): Returns the name of the room where the monster is located.
    """
    def __init__(self, name, description, position=None):
        self.name = name
        self.description = description
        self.position = None # will be set to a room object

    def set_position(self, room): # accepts room object as argument
        self.position = room

    def get_monster_position(self): # returns the name of the room the monster is in
        return self.position.get_room_name()   


class Player:
    """
    Represents a player in the game.

    Args:
        name (str): The name of the player.
        description (str): The description of the player.
    
    Methods:
        set_position(room): Sets the position of the player to a specific room.
        get_player_position(): Returns the name of the room where the player is located.
        get_player_name(): Returns the name of the player.
        get_status(): Returns a tuple of the player's status (alive, escaped).
        player_hit(): Sets the player's alive status to False.
        player_escape(): Sets the player's escaped status to True.
        drop_scent(): Increases the scent of the room the player is in by 3.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.position = None 
        self.alive = True
        self.escaped = False
        #self.has_key = False

    def set_position(self, room): # takes a room object as argument
        self.position = room 

    def get_player_position(self): # returns the name of the room the player is in
        return self.position.get_room_name()
    
    def get_player_name(self):
        return self.name

    def get_status(self): # used in game_functions.py in ending_page function
        return self.alive, self.escaped
    
    def player_hit(self): # used in game_functions in monster_encounter function
        self.alive = False

    def player_escape(self): # called in game_functions in exit_check function
        self.escaped = True
    
    def drop_scent(self): 
        self.position.scent += 3


class Key:
    """
    Represents a key in the game.

    Args:
        name (str): The name of the key.
        description (str): The description of the key.

    Methods:
        set_position(room): Sets the position of the key to a room object
        get_key_position(): Returns the name of the room where the key is located.
        pick_up(): Picks up the key and removes it from its current position.
        key_check(): Checks if the key has been picked up.
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.position = None
        self.picked_up = False

    def set_position(self, room):
        self.position = room

    def get_key_position(self):
        if self.position is not None: # if key has been picked up, it will have no position
            return self.position.get_room_name()
        
    def pick_up(self):
        self.picked_up = True
        self.position = None
    
    def key_check(self):
        return self.picked_up
    
# will track our current game state so we can save this state to a pickle file and load it later
class GameState:
    """
    Represents the state of all the objects in the game

    Args:
        player_object: The player object in the game.
        monster_object: The monster object in the game.
        key_object: The key object in the game.
        room_list: List of room objects in the game.

    """
    def __init__(self, player_object, monster_object, key_object, room_list):
        self.rooms = room_list                   # save the list of room objects
        self.player = player_object           # save the player object
        self.monster = monster_object              # save the monster object
        self.key = key_object                  # save the key object
    

# Considering implementing classes to handle start, game, and end screens, ignore for now
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

    