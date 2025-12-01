import json

with open("data.json", "r") as f:
    data = json.load(f)

def get_ships(data,player:int,ship:int) -> dict:
    return data['game']['player_'+str(player)]['ships'][str(ship)]

def reset_grid(x = 10,y = 5,z = 3):
    grille = [[["-" for _ in range(x)] for _ in range(y)] for _ in range(z)]
    for i in range(1,3):
        data['game']['player_'+str(i)]['grid'] = grille
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
    
def get_grid(player:int):
    return data['game']['player_'+str(player)]['grid']

def add_grid(grid:list,player:int):
    data['game']['player_'+str(player)]['grid'] = grid
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

def get_state():
    return data['game']['state']
