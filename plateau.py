from uuid import uuid4
from music import *

class Boat:
    def __init__(self, name: str, positions: list[tuple[int, int, int]] = [], hits: list[tuple[int, int, int]] = []):
        self.id: str = str(uuid4())
        self.name: str = name
        self.positions: list[tuple[int, int, int]] = positions
        self.hits: list[tuple[int, int, int]] = hits
        self.size: int = len(self.positions)

    def init_boat_pos(self, positions: list[tuple[int, int, int]]):
        """Initialize the boat's positions and size."""
        self.positions = positions
        self.size = len(positions)

    def is_sunk(self) -> bool:
        """Check if the boat is sunk."""
        return len(self.hits) == self.size

class Cell:
    def __init__(self):
        self.boat: Boat | None = None
        self.hit: bool = False
        self.revealed: bool = False
        self.adjacent_revealed: bool = False

    def __str__(self):
        """Return the string representation of the cell for the owner's view."""
        if self.boat is not None:
            if self.boat.is_sunk():
                return 'C '  # Ship sunk
            elif self.hit:
                return 'T '  # Ship hit but not sunk
            else:
                return 'B '  # Ship present but not hit
        else:
            if self.revealed:
                return 'V ' if self.adjacent_revealed else 'R '  # Revealed cell with/without adjacent ship
            else:
                return '. '  # Unrevealed cell
            
    def opponent_str(self) -> str:
        """Return the string representation of the cell for the opponent's view."""
        if self.hit:
            if self.boat is not None:
                return 'C ' if self.boat.is_sunk() else 'T '  # Ship on cell sunk or hit
            else:
                return 'V ' if self.adjacent_revealed else 'R '  # Missed shot revealed with/without adjacent ship
        elif self.revealed:
            return 'V ' if self.adjacent_revealed else 'R '  # Revealed cell with/without adjacent ship
        else:
            return '. '  # Unrevealed cell

class Grid:
    def __init__(self, width: int, height: int, depth: int = 0):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width + 1)] for _ in range(height + 1)]
        self.depth: int = depth

    def display(self, owner_view: bool = True):
        """Display the grid from the owner's or opponent's view."""
        f_row = '  '
        f_row += ''.join(f'{chr(ord("A") + x)} ' for x in range(self.width + 1))
        print(f_row)
        for y in range(self.height + 1):
            row = f'{y} '
            for x in range(self.width + 1):
                row += str(self.cells[y][x]) if owner_view else self.cells[y][x].opponent_str()
            print(row)
        print()

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the plateau bounds."""
        return 0 <= x <= self.width and 0 <= y <= self.height
    
    def boat_fits(self, boat: Boat) -> bool:
        for bx, by, bz in boat.positions:
            if not self.is_within_bounds(bx, by):
                return False
        return True

    def place_boat(self, boat: Boat):
        if not self.boat_fits(boat):
            print("Boat does not fit in the given position.")
            return
        for x, y, _ in boat.positions:
            self.cells[y][x].boat = boat

    def shoot(self, x: int, y: int) -> int:
        print(f"Shooting at ({x}, {y}, {self.depth})")
        torpille_sound()
        sleep(2)
        if not self.is_within_bounds(x, y):
            print("Shot is out of bounds.")
            return -1
        cell = self.cells[y][x]
        if cell.hit:
            print("Ship already hit.")
            return -1
        if cell.boat is None:
            print("Miss!")
            return 0
        else:
            cell.hit = True
            cell.boat.hits.append((x, y))

            explosion_sound()
            print("Hit!")
            return 1

class Plateau:
    def __init__(self, width, height, depth):
        self.width: int = width
        self.height: int = height
        self.depth: int = depth
        self.grids: list[Grid] = [Grid(width, height, z) for z in range(depth)]

    def is_within_bounds(self, x, y, z):
        """Check if the given coordinates are within the plateau bounds."""
        return 0 <= z < self.depth and self.grids[z].is_within_bounds(x, y)
    
    def display(self, owner_view: bool = True):
        """Display the plateau from the owner's or opponent's view."""
        print(f"======== {'Owner' if owner_view else 'Opponent'}'s View ========")
        for z in range(self.depth):
            print(f"{(z+1)*100}m")
            self.grids[z].display(owner_view=owner_view)
        print("="*20)

    def display_version2(self, owner_view: bool = True):
        """Display the plateau from the owner's or opponent's view."""

        # Titre principal
        print("┌" + "─" * 46 + "┐")
        print(f"│        {'  OWNER ' if owner_view else 'OPPONENT'}'S VIEW OF THE PLATEAU        │")
        print("└" + "─" * 46 + "┘\n")

        # Affichage de chaque niveau
        for z in range(self.depth):
            depth_label = f"{(z + 1) * 100}m"

            print("┌" + "─" * 20 + f" {depth_label:^8} " + "─" * 20 + "┐")
            self.grids[z].display(owner_view=owner_view)
            print("└" + "─" * 50 + "┘\n")

        # Ligne de fin
        print("═" * 52)


    def place_boat(self, position: tuple[int, int, int], size: int, is_horizontal: bool, boat: Boat):
        """Place a boat at the given position with specified orientation and size."""
        sx, sy, sz = position
        print(f"Placing boat at ({sx}, {sy}, {sz}), size: {size}, horizontal: {is_horizontal}")
        if not self.is_within_bounds(sx, sy, sz):
            print("Boat placement is out of bounds.")
            return
        boat.init_boat_pos([(sx + i, sy, sz) for i in range(size)] if is_horizontal else [(sx, sy + i, sz) for i in range(size)])
        self.grids[sz].place_boat(boat)

    def shoot(self, x: int, y: int, z: int):
        shot = self.grids[z].shoot(x, y)
        if shot == 0:
            self.reveal_cells((x, y, z))
        else:
            pass
    
    def reveal_cells(self, position: tuple[int, int, int]):
        """Reveal the cell at the given position and its adjacent cells."""
        x, y, z = position
        to_check_positions = [(x, y, z), (x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
        reveal_cells = False
        for cx, cy, cz in to_check_positions:
            if not self.is_within_bounds(cx, cy, cz):
                to_check_positions.remove((cx, cy, cz))
            else:
                if self.grids[cz].cells[cy][cx].boat is not None and not self.grids[cz].cells[cy][cx].hit:
                    reveal_cells = True
        for cx, cy, cz in to_check_positions:
            cell = self.grids[cz].cells[cy][cx]
            if cell.revealed and not cell.adjacent_revealed:
                continue
            cell.revealed = True
            sonar_sound()
            cell.adjacent_revealed = reveal_cells
            
# if __name__ == "__main__":
#     plateau = Plateau(5, 5, 2)
#     boat = Boat("Bato")
#     plateau.place_boat((3, 3, 0), 3, False, boat)
#     plateau.place_boat((1, 0, 0), 2, False, boat)
#     plateau.place_boat((3, 1, 1), 1, True, boat)
#     plateau.display()
#     plateau.display(False)
#     plateau.shoot(3, 2, 0)
#     plateau.display()
#     plateau.display(False)
    