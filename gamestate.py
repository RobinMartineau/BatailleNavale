import time
from plateau import *
from uuid import uuid4

class Player:
    def __init__(self, name: str):
        self.id = str(uuid4())
        self.name: str = name
        self.ships: list[Boat] = []
        self.plateau: Plateau | None = None

class GameState:
    def __init__(self, p1: Player, p2: Player, plateau_size: tuple[int, int, int] = (7, 5, 3)):
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

    def switch_turn(self):
        """Switch the current turn to the other player."""
        if self.current_turn == self.p1.id:
            self.current_turn = self.p2.id
        else:
            self.current_turn = self.p1.id
        self.turns += 1