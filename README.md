# hescape
hescape is a mini horror game that has a player explore a small map while avoiding a monster and find a way to escape

## Features
- Command-line gameplay with Object-Oriented Programming principles.
- A dynamically generated map for exploration.
- Monster pathfinding that adds tension and challenge.
- Game logic tested for:
  - Map validity.
  - Monster movement accuracy.
 
## Game Mechanics
- Objective: Explore the map, avoid the monster, find the key, and escape.
- Monster Behavior: The monster uses pathfinding to track the player's movements, adding tension to the gameplay.
- Player Commands: Players input commands to move, inspect rooms, and interact with objects.

## Future Improvements
- A GUI interface built using PyQt5 with three screens:
  - Start Screen: Game introduction and start button.
  - Game Screen: Displays game updates and accepts player commands.
  - End Screen: Game-over screen with options to restart or exit.

-Data Integration:
  - Implement a database (e.g., SQLite) to store player scores or game states.
  - Create a REST API for multiplayer functionality or saving progress.
