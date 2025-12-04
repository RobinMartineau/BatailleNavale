import time
from plateau import *

class GameState:
    def __init__(self, p1_name: str, p2_name: str, plateau_size: tuple[int, int, int] = (7, 5, 3)):
        self.p1: str = p1_name
        self.p2: str = p2_name
        
        # Init both players empty plateau
        self.p1_plateau = Plateau(*plateau_size)
        self.p2_plateau = Plateau(*plateau_size)

        # Timestamps
        self.started_at: float = time.time()
        self.ended_at: float | None = None

        # Miscs
        self.turns = 0
        self.current_turn: str = p1_name
        self.phase: str = 'placement'
        self.winner: str | None = None

    def switch_turn(self):
        """Switch the current turn to the other player."""
        if self.current_turn == self.p1:
            self.current_turn = self.p2
        else:
            self.current_turn = self.p1
        self.turns += 1