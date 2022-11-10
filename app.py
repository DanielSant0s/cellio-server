from flask import Flask, request

app = Flask(__name__)

players = []

def distance(p1, p2):
    distX = p1['coords'][0] - p2['coords'][0]
    distY = p1['coords'][1] - p2['coords'][1]
    dist = ((distX**2) + (distY**2)) ** (1/2)
    if dist <= (p1['radius'] + p2['radius']):
        return True
    return False

@app.route('/')
def hello_world():
    return 'cell.io prototype test'

@app.route("/player")
def update_player():
    player_name = request.args.get("name")
    player_x = request.args.get("x")
    player_y = request.args.get("y")
    player_r = request.args.get("r")
    player = {}

    player_idx = next((i for i in range(len(players)) if players[i]['name'] == player_name), -1)

    if player_idx != -1:
        players.remove(players[player_idx])
        if players[player_idx]['alive'] == False:
            return (False, 0)

    player['name'] = player_name
    player['coords'] = (player_x, player_y)
    player['radius'] = player_r
    player['alive'] = True

    for enemy in players:
        if distance(player, enemy):
            if player['radius'] > enemy['radius']:
                enemy_idx = players.index(enemy)
                players[enemy_idx]['alive'] = False
                player['radius'] += enemy['radius']/2
            elif enemy['radius'] > player['radius'] :
               return (False, 0)

    players.append(player)

    return str([True, player['radius']])

@app.route("/get")
def get_players():
    return str(players)

if __name__ == '__main__':
    app.run()