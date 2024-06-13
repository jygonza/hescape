import pytest
from game_functions import path_decay
from unittest.mock import MagicMock
# Sample Room class to be used in tests
class Room:
    def __init__(self, scent):
        self.scent = scent

    def dissipate_scent(self):
        self.scent -= 1

    def get_scent(self):
        return self.scent

@pytest.mark.parametrize(
    "scent_path, rooms, expected_scent_path",
    [
        # Happy path tests
        (["room1", "room2"], {"room1": Room(2), "room2": Room(3)}, ["room1", "room2"]),  # happy_path_1
        (["room1", "room2"], {"room1": Room(1), "room2": Room(1)}, []),  # happy_path_2
        
        # Edge cases
        ([], {"room1": Room(2)}, []),  # empty_scent_path
        (["room1"], {"room1": Room(1)}, []),  # single_room_zero_scent
        (["room1"], {"room1": Room(2)}, ["room1"]),  # single_room_non_zero_scent
        
        # Error cases
        (["room1"], {"room1": Room(0)}, []),  # room_with_initial_zero_scent
        (["room1", "room2"], {"room1": Room(1), "room2": Room(0)}, []),  # mixed_scent_levels
    ]
)
def test_path_decay(scent_path, rooms, expected_scent_path):
    # Act
    path_decay(scent_path, rooms)
    # Assert
    assert scent_path == expected_scent_path


