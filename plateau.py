from uuid import uuid4
from music import *

RESET = "\033[0m"
CYAN = "\033[36m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
BOLD = "\033[1m"
GREY = "\033[90m"

def cell_str_owner(cell):
    """Return styled cell for owner view."""
    if cell.boat:
        if cell.boat.is_sunk():
            return f"{RED}C {RESET}"   # Coulé
        if cell.hit:
            return f"{RED}T {RESET}"   # Touché
        return f"{GREEN}B {RESET}"     # Bateau non touché
    else:
        if cell.revealed:
            if cell.adjacent_revealed:
                return f"{CYAN}V {RESET}"  # Vide proche bateau
            return f"{BLUE}R {RESET}"      # Révélé vide
        return ". "  # inconnu


def cell_str_enemy(cell):
    """Return styled cell for enemy view."""
    if cell.hit:
        if cell.boat is not None:
             return f"{RED}C {RESET}" if cell.boat.is_sunk() else f"{RED}T {RESET}"  # Ship on cell sunk or hit
        else:
            return f"{CYAN}V {RESET}" if cell.adjacent_revealed else f"{BLUE}R {RESET}"  # Missed shot revealed with/without adjacent ship
    elif cell.revealed:
        return f"{CYAN}V {RESET}" if cell.adjacent_revealed else f"{BLUE}R {RESET}"  # Revealed cell with/without adjacent ship
    else:
        return '. '  # Unrevealed cell

class Boat:
    def __init__(self, name: str, positions: list[tuple[int, int, int]] | None = None, hits: list[tuple[int, int, int]] | None = None):
        self.id: str = str(uuid4())
        self.name: str = name
        self.positions: list[tuple[int, int, int]] = [tuple(pos) for pos in positions] if positions else []
        self.hits: list[tuple[int, int, int]] = [tuple(hit) for hit in hits] if hits else []
        self.size: int = len(self.positions)

    def init_boat_pos(self, positions: list[tuple[int, int, int]]):
        """Initialize the boat's positions and size."""
        self.positions = positions
        self.size = len(positions)

    def is_sunk(self) -> bool:
        """Check if the boat is sunk."""
        return len(self.hits) >= self.size
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "positions": self.positions,
            "hits": self.hits,
            "size": self.size
        }
    
    def from_dict(id: str, data: dict) -> 'Boat':
        boat = Boat(data["name"], data["positions"], data["hits"])
        boat.size = data.get("size") or len(boat.positions)
        boat.id = id
        return boat

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
        
    def to_dict(self) -> dict:
        return {
            "boat": self.boat.id if self.boat else None,
            "hit": self.hit,
            "revealed": self.revealed,
            "adjacent_revealed": self.adjacent_revealed
        }

class Grid:
    def __init__(self, width: int, height: int, depth: int = 0):
        self.width = width
        self.height = height
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
        self.depth: int = depth

    def displayAncienneVers(self, owner_view: bool = True):
        """Display the grid from the owner's or opponent's view."""
        f_row = '  '
        f_row += ''.join(f'{chr(ord("A") + x)} ' for x in range(self.width))
        print(f_row)
        for y in range(self.height):
            row = f'{y} '
            for x in range(self.width):
                row += str(self.cells[y][x]) if owner_view else self.cells[y][x].opponent_str()
            print(row)
        print()

    def display(self, owner_view: bool = True):
        """Beautiful and modern display for a single grid layer."""

        # Ligne des colonnes (A B C ...)
        header = "    "  # espace pour le y
        for x in range(self.width + 1):
            header += f"{GREY}{chr(ord('A') + x)} {RESET}"
        print(header)

        # Ligne horizontale
        print("   " + "─" * (2 * (self.width + 1)))

        # Corps de la grille
        for y in range(self.height + 1):
            row = f"{YELLOW}{y:<2}{RESET} "  # numéro de la ligne

            for x in range(self.width + 1):
                cell = self.cells[y][x]
                if owner_view:
                    row += cell_str_owner(cell)
                else:
                    row += cell_str_enemy(cell)

            print(row)

        print()


    def is_within_bounds(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the plateau bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    
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
            cell.boat.hits.append((x, y, self.depth))

            explosion_sound()
            print("Hit!")
            return 1
        
    def to_array(self) -> dict:
        return [[cell.to_dict() for cell in row] for row in self.cells]

    def is_sunk(self):
        return all(pos in self.hits for pos in self.positions)

    
class Plateau:
    def __init__(self, width, height, depth):
        self.width: int = width
        self.height: int = height
        self.depth: int = depth
        self.grids: list[Grid] = [Grid(width, height, z) for z in range(depth)]

    def is_within_bounds(self, x, y, z):
        """Check if the given coordinates are within the plateau bounds."""
        return 0 <= z < self.depth and self.grids[z].is_within_bounds(x, y)
    
    def displayAncienneVersion(self, owner_view: bool = True):
        """Display the plateau from the owner's or opponent's view."""
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

    def display(self, owner_name, opp_name, owner_view: bool = True):
        """Beautiful styled display for the plateau."""

        title = f"PLATEAU DE {owner_name}" if owner_view else f"PLATEAU DE {owner_name} VU PAR {opp_name}"
        border_top = "┌" + "─" * 48 + "┐"
        border_bottom = "└" + "─" * 48 + "┘"

        print()
        print(border_top)
        print(f"│{BOLD}{CYAN}{title:^48}{RESET}│")
        print(border_bottom)
        print()

        for z in range(self.depth):
            depth_label = f"{(z+1)*100}m"

            # ── HEADER DU NIVEAU ────────────────────────────────
            print(f"{BLUE}{BOLD}LEVEL {depth_label:^8}{RESET}")
            print(f"{BLUE}{BOLD}┌" + "─" * (4 + 2 * (self.width)) + "┐" + RESET)

            # Coordonnées X (colonnes)
            header = f"{BLUE}│{RESET}    "  # espace pour le Y
            for x in range(self.width):
                header += f"{GREY}{chr(ord('A') + x)} {RESET}"
            header += f"{BLUE}│{RESET}"
            print(header)

            print(f"{BLUE}│{RESET}" + "─" * (4 + 2 * (self.width)) + f"{BLUE}│{RESET}")  # ligne horizontale

            # LIGNES DU PLATEAU
            for y in range(self.height):
                row = f"{BLUE}│{RESET} {YELLOW}{y}{RESET}  "
                for x in range(self.width):
                    cell = self.grids[z].cells[y][x]

                    if owner_view:
                        row += cell_str_owner(cell)
                    else:
                        row += cell_str_enemy(cell)

                row += f"{BLUE}│{RESET}"
                print(row)

            print(f"{BLUE}{BOLD}└" + "─" * (4 + 2 * (self.width)) + "┘" + RESET)
            print()

    def place_boat(self, position: tuple[int, int, int], size: int, is_horizontal: bool, boat: Boat):
        """Place a boat at the given position with specified orientation and size."""
        sx, sy, sz = position
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
        x, y, z = position

        to_check_positions = [
            (x, y, z),
            (x + 1, y, z), (x - 1, y, z),
            (x, y + 1, z), (x, y - 1, z),
            (x, y, z + 1), (x, y, z - 1)
        ]

        valid_positions = [
            (cx, cy, cz)
            for cx, cy, cz in to_check_positions
            if self.is_within_bounds(cx, cy, cz)
        ]

        reveal_adjacent = False
        for cx, cy, cz in valid_positions:
            try:
                cell = self.grids[cz].cells[cy][cx]
                if cell.boat is not None and not cell.hit:
                    reveal_adjacent = True
                    break
            except IndexError:
                continue

        for cx, cy, cz in valid_positions:
            try:
                cell = self.grids[cz].cells[cy][cx]
                cell.revealed = True
                cell.adjacent_revealed = reveal_adjacent
            except IndexError:
                continue

    def to_dict(self) -> dict:
        return {f"{i}": grid.to_array() for i, grid in enumerate(self.grids)}
    
    def from_dict(data: dict, boats: list[Boat]) -> 'Plateau':
        depth = len(data)
        width = len(data["0"][0]) - 1
        height = len(data["0"]) - 1
        plateau = Plateau(width, height, depth)
        for z_str, grid_data in data.items():
            z = int(z_str)
            for y in range(height):
                for x in range(width):
                    cell_data = grid_data[y][x]
                    cell = plateau.grids[z].cells[y][x]
                    cell.hit = cell_data["hit"]
                    cell.revealed = cell_data["revealed"]
                    cell.adjacent_revealed = cell_data["adjacent_revealed"]
                    cell.boat = next((boat for boat in boats if boat.id == cell_data["boat"]), None) if cell_data["boat"] else None
        return plateau
