import random
class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        #self.items = {} # not used right now
        self.connected_rooms = {}
    def connect(self, room):
        self.connected_rooms[room.name] = room

    def get_connected_rooms(self):
        return self.connected_rooms
    
    def get_room_description(self):
        return self.description
    
    def get_room_name(self):
        return self.name

    def reset_room(self):
        self.connected_rooms = {}

def connect_rooms(room_list):
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
connect_rooms2(ROOMS)

for room in ROOMS.values():
    print(room.get_room_name())
    for connected_room in room.get_connected_rooms().keys():
        print("\t", connected_room)

import unittest
class TestRoomConnections(unittest.TestCase):
    def dfs(self, room, visited):
        visited.add(room)
        for connected_room in ROOMS[room].get_connected_rooms().keys():
            if connected_room not in visited:
                self.dfs(connected_room, visited)

    def test_connected_graph(self):
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
        connect_rooms2(ROOMS)

        visited = set()
        start_room = next(iter(ROOMS.keys()))  # Get the first room object
        self.dfs(start_room, visited)

        # Check if all rooms have been visited
        self.assertEqual(len(visited), len(ROOMS))

if __name__ == "__main__":
    unittest.main()

