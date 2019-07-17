import random

class VictorPilleur:

	def __init__(self, config):
		self.log = []
		self.config = config
		self.lastShot = (-1, -1)
		self.target = []

	def controller(self, gameMap):
		
		#premier coup
		if len(self.log) == 0:
			self.lastShot = self.getRandom()
			return self.lastShot
		#si on vient de toucher un bateau
		elif self.log[-1][2] == True:
			self.target = []
			self.setTarget(self.log[-1][0], self.log[-1][1])
			if len(self.target ) == 0:
				self.lastShot = self.getRandom()
				return self.lastShot
			self.lastShot = self.target[random.randint(0, len(self.target) - 1)]
			return self.lastShot
		else:
			self.lastShot = self.getRandom()
			return self.lastShot

	# recoit le retour du tir
	def transferAnswer(self, touch):
		self.addLog(touch)

	# log = (xpos, ypos, touch=bool)
	def addLog(self, touch):
		self.log.append((self.lastShot[0], self.lastShot[1], touch))

	# cherche dans les logs si la position envoyé a deja été testé
	def isAlreadyTest(self, x, y):
		for log in self.log:
			if log[0] == x and log[1] == y:
				return True
			else:
				return False

	# alimente la liste de position cible
	def setTarget(self, x, y):

		nearImpact = []

		for log in self.log:
			if (log[0] == x - 1 and log[1] == y) or (log[0] == x and log[1] == y - 1) or (log[0] == x + 1 and log[1] == y) or (log[0] == x and log[1] == y + 1):
			    if log[2]: 
			    	nearImpact.append((x, y))

		if len(nearImpact) == 1:
			if x == nearImpact[0][0]:
				self.target.append((x, y - 1))
				self.target.append((x, y + 1))
			else:
				self.target.append((x - 1, y))
				self.target.append((x + 1, y))

		elif len(nearImpact) == 0:
			self.target.append((x - 1, y))
			self.target.append((x, y - 1))
			self.target.append((x + 1, y))
			self.target.append((x, y + 1))

		
		i = 0
		while i < len(self.target):
			if self.isAlreadyTest(self.target[i][0], self.target[i][1]) or self.target[i][0] > self.config["size"] - 1 or self.target[i][1] > self.config["size"] - 1 or self.target[i][0] < 0 or self.target[i][1] < 0:
				del self.target[i]
			i += 1

	# retourne une case de la zone la moins bombardé
	def getRandom(self):

		absc = [0] * self.config["size"]
		ordo = [0] * self.config["size"]

		for log in self.log:
			absc[log[0]] += 1
			ordo[log[1]] += 1

		minAbs = absc[0]
		indMinAbs = 0
		i = 1
		while i < len(absc):
			if absc[i] < minAbs:
				minAbs = absc[i]
				indMinAbs = i
			i += 1

		minOrd = ordo[0]
		indMinOrd = 0
		i = 1
		while i < len(ordo):
			if ordo[i] < minOrd:
				minOrd = ordo[i]
				indMinOrd = i
			i += 1


		while(self.isAlreadyTest(indMinAbs, indMinOrd)):
			indMinAbs = random.randint(0, self.config["size"] - 1)
			indMinOrd = random.randint(0, self.config["size"] - 1)

		return indMinAbs, indMinOrd

