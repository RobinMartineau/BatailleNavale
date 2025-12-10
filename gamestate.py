import time
from plateau import *
from uuid import uuid4
import json
import os
from pathlib import Path

GAMESTATES_DIR = "./saved_games/"

class Player:
    def __init__(self, name: str):
        self.id: str = str(uuid4())
        self.name: str = name
        self.boats: list[Boat] = []
        self.plateau: Plateau | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "boats": {f"{boat.id}": boat.to_dict() for boat in self.boats},
            "plateau": self.plateau.to_dict() if self.plateau else None,
        }
    
    def init_from_dict(self, data: dict):
        self.name = data["name"]
        self.boats = [Boat.from_dict(boat_data) for boat_data in data["boats"].values()]
        if data["plateau"]:
            self.plateau = Plateau.from_dict(data["plateau"], self.boats)
        else:
            self.plateau = None

class GameState:
    def __init__(self, p1: Player, p2: Player, plateau_size: tuple[int, int, int] = (7, 5, 3)):
        self.id: str = str(uuid4())
        self.p1: Player = p1
        self.p2: Player = p2
        
        # Init both players empty plateau
        self.p1.plateau = Plateau(*plateau_size)
        self.p2.plateau = Plateau(*plateau_size)

        # Timestamps
        self.started_at: float = time.time()
        self.ended_at: float | None = None

        # Miscs
        self.turns = 0
        self.current_turn: str = p1.id
        self.phase: str = 'placement'
        self.winner: str | None = None

        self.config: dict = {
            "plateau_size": plateau_size,
        }

    def switch_turn(self):
        """Switch the current turn to the other player."""
        if self.current_turn == self.p1.id:
            self.current_turn = self.p2.id
        else:
            self.current_turn = self.p1.id
        self.turns += 1

    def load_json(self, id: str):
        """Initialize the game state from a JSON-like dictionary."""
        file_path = os.path.join(GAMESTATES_DIR, f"{id}.json")
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Gamestate file not found: {file_path}")
        with open(file_path, 'r') as f:
            gamestate_dict = json.load(f)
        
        self.id = id
        self.started_at = gamestate_dict["started_at"]
        self.ended_at = gamestate_dict["ended_at"]
        self.turns = gamestate_dict["turns"]
        self.current_turn = gamestate_dict["current_turn"]
        self.phase = gamestate_dict["phase"]
        self.winner = gamestate_dict["winner"]
        self.p1.init_from_dict(gamestate_dict["players"][list(gamestate_dict["players"].keys())[0]])
        self.p2.init_from_dict(gamestate_dict["players"][list(gamestate_dict["players"].keys())[1]])


    def save_gamestate(self):
        """Save the current game state to a JSON-like dictionary."""
        savedGamesDirPath = Path(GAMESTATES_DIR)
        if not savedGamesDirPath.exists():
            os.makedirs(savedGamesDirPath)
        file_path = os.path.join(GAMESTATES_DIR, f"{self.id}.json")
        
        gamestate_dict = self.to_dict()

        gamestate_json = json.dumps(gamestate_dict, indent=4)

        with open(file_path, 'w') as f:
            f.write(gamestate_json)

    def to_dict(self) -> dict:
        return {
            "title": "",
            "started_at": self.started_at,
            "ended_at": self.ended_at or None,
            "turns": self.turns,
            "current_turn": self.current_turn,
            "phase": self.phase,
            "winner": self.winner or None,
            "players": {f"{player.id}": player.to_dict() for player in [self.p1, self.p2]},
            "config": {}
        }
    
if __name__ == "__main__":
    p1 = Player("Alice")
    p2 = Player("Bob")
    gamestate = GameState(p1, p2)
    gamestate.save_gamestate()