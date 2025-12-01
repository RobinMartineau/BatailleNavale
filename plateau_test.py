class Boat:
    def __init__(self, name: str, size: int, horizontal: bool):
        self.name = name
        self.size = size
        self.horizontal = horizontal
        self.hits = []
        self.positions = []

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(width + 1)] for _ in range(height + 1)]

    def display_struct(self, current_depth=0):
        for y in range(self.height + 1):
            row = ''
            for x in range(self.width + 1):
                row += f'({x},{y},{current_depth}) '
            print(row)
        print()
        
        for cell in self.cells:
            for boat in cell:
                if boat is not None:
                    print(f'Boat: {boat.name}, Size: {boat.size}, Horizontal: {boat.horizontal}, Hits: {boat.hits}')

    def display_for_owner(self):
        print('  ', end='')
        for x in range(self.width + 1):
            print(f'{chr(ord("A") + x)} ', end='')
        print()
        for y in range(self.height + 1):
            row = f'{y} '
            for x in range(self.width + 1):
                cell = self.cells[y][x]
                if cell is None:
                    row += '. '
                else:
                    row += f'{cell.name[0]} '
            print(row)
        print()

    def display_for_opponent(self):
        print('  ', end='')
        for x in range(self.width + 1):
            print(f'{chr(ord("A") + x)} ', end='')
        print()
        for y in range(self.height + 1):
            row = f'{y} '
            for x in range(self.width + 1):
                cell = self.cells[y][x]
                if cell is None or (x, y) not in cell.hits:
                    row += '. '
                else:
                    row += 'X '
            print(row)
        print()

    def is_within_bounds(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the plateau bounds."""
        return 0 <= x <= self.width and 0 <= y <= self.height
    
    def boat_fits(self, x: int, y: int, boat: Boat) -> bool:
        for i in range(boat.size):
            if not self.is_within_bounds(x + i if boat.horizontal else x, y if boat.horizontal else y + i):
                return False
        return True

    def place_boat(self, x: int, y: int, boat: Boat):
        if not self.boat_fits(x, y, boat):
            print("Boat does not fit in the given position.")
            return
        for i in range(boat.size):
            if boat.horizontal:
                self.cells[y][x + i] = boat
            else:
                self.cells[y + i][x] = boat

    def shoot(self, x: int, y: int) -> bool:
        if not self.is_within_bounds(x, y):
            print("Shot is out of bounds.")
            return False
        cell = self.cells[y][x]
        if cell is None:
            print("Miss!")
            return False
        else:
            cell.hits.append((x, y))
            print("Hit!")
            return True

class Plateau:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.grids = [Grid(width, height) for _ in range(depth)]

    def is_within_bounds(self, x, y, z):
        """Check if the given coordinates are within the plateau bounds."""
        return 0 <= z <= self.depth and self.grids[z].is_within_bounds(x, y)
    
    def display_struct(self):
        for z in range(self.depth):
            print(f"Grid at depth {z}:")
            self.grids[z].display_struct(z)

    def display_for_owner(self):
        for z in range(self.depth):
            print(f"Grid at depth {z}:")
            self.grids[z].display_for_owner()

    def display_for_opponent(self):
        for z in range(self.depth):
            print(f"Grid at depth {z}:")
            self.grids[z].display_for_opponent()

    def shoot(self, x: int, y: int, z: int):
        pass
            

if __name__ == "__main__":
    plateau = Plateau(5, 5, 1)
    boat = Boat("Bato", 3, False)
    plateau.grids[0].place_boat(3, 3, boat)
    plateau.display_for_owner()
    plateau.display_for_opponent()
    plateau.shoot(3, 3, 0)
    plateau.display_for_opponent()
    plateau.display_struct()
