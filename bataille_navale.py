import random

config = {
    "size":10,
	"ships": {
		2: 2,
		3: 1,
		4: 1,
		5: 1
	},
	"ship_one_beside_other": False,
	"aiPlayer1": "naive",
	"aiPlayer2": "naive"
}

def initMap():
	gameMap = []
	for i in range(config['size']):
		gameMap.append([0] * config['size'])
	ships = []
	ship_id = 0
	for ship_size in config['ships']:
		ship_count = config['ships'][ship_size]
		for i in range(ship_count):
			isVertical = random.randint(0, 100) % 2
			valid = False
			for attempt in range(1000):
				# random coords
				x1 = random.randint(0, config['size'] - 1)
				y1 = random.randint(0, config['size'] - 1)
				x2 = x1 + ship_size - 1 if not isVertical else x1
				y2 = y1 + ship_size - 1 if isVertical else y1
				# check coords
				if (x2 >= config['size'] or y2 >= config['size']):
					continue
				_valid = True
				for x in range(x1, x2 + 1):
					for y in range(y1, y2 + 1):
						if gameMap[x][y] != 0: _valid = False
						if not config['ship_one_beside_other']:
							if x > 0 and gameMap[x - 1][y] != 0: _valid = False
							if x < config['size'] - 1 and gameMap[x + 1][y] != 0: _valid = False
							if y > 0 and gameMap[x][y - 1] != 0: _valid = False
							if y < config['size'] - 1 and gameMap[x][y + 1] != 0: _valid = False
				if not _valid:
					continue
				ship_id += 1
				ships.append({
					'id': ship_id,
					'coords': {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2},
					'life': ship_size
				})
				for x in range(x1, x2 + 1):
					for y in range(y1, y2 + 1):
						gameMap[x][y] = ship_id
				valid = True
				break
			if not valid:
				print("Map Initialization failed!")
				quit()
	gameMap = []
	for i in range(config['size']):
		gameMap.append([0] * config['size'])
	return ships, gameMap

"""
isShipPosition
"""
def isShipPosition(x, y, currentShips):

	ships = currentShips

	for ship in ships:
		if ship['coords']['x1'] <= x <= ship['coords']['x2']:
			if ship['coords']['y1'] <= y <= ship['coords']['y2']:
				return True
	return False

"""
getShip (with one of its coords)
"""
def getShip(x, y, currentShips):

	ships = currentShips

	for ship in ships:
		if ship['coords']['x1'] <= x <= ship['coords']['x2']:
			if ship['coords']['y1'] <= y <= ship['coords']['y2']:
				return ship
	return None

"""
isAllShipDead
"""
def isAllShipDead(currentShips):

	ships = currentShips

	for ship in ships:
		if ship['life'] > 0:
			return False
	return True

"""
numberOfBoatsAlive
"""

def numberAliveShips(currentShips):

	ships = currentShips
	i = 0
	for ship in ships:
		if ship['life'] > 0:
			i += 1
	return i

"""
Print the game and shot cases
"""

def print_board(gameMapPlayer1, gameMapPlayer2):
	print(" 0 1 2 3 4 5 6 7 8 9 || 0 1 2 3 4 5 6 7 8 9")
	for row in range(config['size']):
		print(gameMapPlayer1[row], end = ' || ')
		print(gameMapPlayer2[row])

def main():

	shipsPlayer1, gameMapPlayer1 = initMap()
	shipsPlayer2, gameMapPlayer2 = initMap()

	playerTurn = True

	while(True):

		if (playerTurn):
			
			if (config['aiPlayer1'] == 'naive'):
				
				while True:
					xShot = random.randint(0, config['size'] - 1)
					yShot = random.randint(0, config['size'] - 1)

					if not gameMapPlayer2[xShot][yShot]:
						break

				gameMapPlayer2[xShot][yShot] = 1

				if not isShipPosition(xShot, yShot, shipsPlayer2):
					playerTurn = not playerTurn
					continue
				else:

					ship = getShip(xShot, yShot, shipsPlayer2)
					ship['life'] -= 1

					if ship['life'] == 0:
						print_board(gameMapPlayer1, gameMapPlayer2)
						print('Navire détruit !')
						print('Nombre de navire(s) joueur 2', end = ' : ')
						print(numberAliveShips(shipsPlayer2))

					if isAllShipDead(shipsPlayer2):
						print('Victoire du joueur 1 !!!')
						quit()
					playerTurn = not playerTurn
		else :
				
			if (config['aiPlayer2'] == 'naive'):
				while True:
					xShot = random.randint(0, config['size'] - 1)
					yShot = random.randint(0, config['size'] - 1)

					if not gameMapPlayer1[xShot][yShot]:
						break

				gameMapPlayer1[xShot][yShot] = 1

				if not isShipPosition(xShot, yShot, shipsPlayer1):						
					playerTurn = not playerTurn
					continue
				else:

					ship = getShip(xShot, yShot, shipsPlayer1)
					ship['life'] -= 1

					if ship['life'] == 0:
						print_board(gameMapPlayer1, gameMapPlayer2)
						print('Navire détruit !')
						print('Nombre de navire(s) joueur 1', end = ' : ')
						print(numberAliveShips(shipsPlayer1))
						
					if isAllShipDead(shipsPlayer1):
						print('Victoire du joueur 2 !!!')
						quit()
					playerTurn = not playerTurn

main()