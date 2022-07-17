#
# Instituto Federal de Educação, Ciência e Tecnologia - IFPE
# Campus: Igarassu
# Curso: Sistemas para Internet
# Disciplina: Metodologia Científica
# Professor: Allan Lima - allan.lima@igarassu.ifpe.edu.br
# 
# Código de Domínio Público, sinta-se livre para usá-lo, modificá-lo e redistribuí-lo.
#


# in case the interpreter does not recognizes the class enum:
# 
# 1) try installing it: sudo pip install enum34
#
# 2) force the code to run on python3: python3 randomWalkModel.py
import enum
import random
# import pandas as pd # dataframes
# import matplotlib.pyplot as plt # plotting data

# df = pd.read_csv("https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv")

from PIL import Image # pip install Pillow

class State(enum.Enum):
	healthy = 0
	sick = 1
	dead = 2
	hospital = 3

class Individual:
	def __init__(self, state):
		self.state = state

class RandomWalkModel:
	def __init__(self, populationMatrixSize): # if the self parameter is always explicit, can we realy say that python is a OO language?
	
		self.population = []
		self.nextPopulation = []
		self.currentGeneration = 0
		
		#
		# 			healthy	sick	dead	hospital
		# healthy	1.0		0.0		0.0		0.0
		# sick		0.4		0.1		0.3		0.0
		# dead		0.0		0.0		0.0		0.0
		# hospital	0.0	    0.0	    0.0	   	0.0
		#
		# notice how there is no transition from the healthy state
		self.transitionProbabilities = [[1.0, 0.0, 0.0, 0.0],
		 								[0.4, 0.1, 0.3, 0.0],
		 								[0.0, 0.0, 0.0, 0.0],
		 								[0.0, 0.0, 0.0, 0.0]]
		self.contagionFactor = 0.256

		for i in range(populationMatrixSize):
			self.population.append([])
			self.nextPopulation.append([])
			for j in range(populationMatrixSize):
				self.population[i].append(Individual(State.healthy))
				self.nextPopulation[i].append(Individual(State.healthy))

		# TODO put the first case at a random position
		startIndex = int(populationMatrixSize/2)
		self.population[startIndex][startIndex].state = State.sick
		self.nextPopulation[startIndex][startIndex].state = State.sick
		#self.nextPopulation[0][0].state = State.sick

	# TODO handle all transitions as function instead of probabilities
	def individualTransition(self, line, column):
		individual = self.population[line][column]

		# optimization
		if (individual.state == State.dead):
			return

		# health people interact each it other
		if (individual.state == State.healthy):
			self.computeSocialInteractions(line, column)

		# if (individual.state == State.hospital):
		# 	print("Hospitalized")

		# other states are handled as a state machine
		else:
			probabilities = self.transitionProbabilities[individual.state.value]
			number = random.random()

			#print(individual, individual.state.value)
			#print(number, probabilities)

			cumulativeProbability = 0
			for index in range(len(probabilities)):
				cumulativeProbability = cumulativeProbability + probabilities[index]
					#print(cumulativeProbability, probabilities[j])
					
				if (number > 0.0 and number <= cumulativeProbability):
					#print('transition from', self.population[index], 'to', State(j))

					# debug code to warn if someone ressurects
					if (individual.state == State.dead):
						print("ERROR: DEATH TRANSITION ", number, cumulativeProbability, index, probabilities[index])

					self.nextPopulation[line][column].state = State(index)
					break

	def computeSickContact(self, individual, neighbour):
		if (individual.state == State.dead):
			print("ERROR: DEATH TRANSITION ", individual, neighbour)

		number = random.random()

		if (number < self.contagionFactor):
			individual.state = State.sick
			#print("change")

	def computeSocialInteractions(self, line, column):
		initialLine = max(0, line - 1)
		finalLine = min(line + 2, len(self.population))
		
		for i in range(initialLine, finalLine):

			initialColumn = max(0, column - 1)
			finalColumn = min(column + 2, len(self.population[i]))

			for j in range(initialColumn, finalColumn):
				neighbour = self.population[i][j]
	
				if (neighbour.state == State.sick):
					#print("sick", line, column, i, j)
					# changes are perfomed only on the next population
					self.computeSickContact(self.nextPopulation[line][column], neighbour)

				# if 	(neighbour.state == State.sick):
				# 	self.computeHospitalized(self.nextPopulation[line][column], neighbour)
				# 	# print("computeSocialInteractions")

	# def computeHospitalized(self, individual, neighbour):
	# 		hospitals = 0

	# 		if (hospitals <= 9):
	# 			individual.state = State.hospital
	# 			hospitals = hospitals + 1
	# 			# print("computeHospitalized<=")

	# 		if (hospitals > 9):
	# 			individual.state = State.sick
	# 			# print("computeHospitalized>")

	# def nextGeneration(self):
	# 	for i in range(len(self.population)):
	# 		for j in range(len(self.population[i])):
	# 			self.individualTransition(i, j)

	# 	for i in range(len(self.population)):
	# 		for j in range(len(self.population[i])):
	# 			self.population[i][j].state = self.nextPopulation[i][j].state
	# 			#print("test")

	def report(self):
		states = list(State)
		cases = []

		for s in states:
			cases.append(0)

		for line in self.population:
			for individual in line:
				cases[individual.state.value] += 1

		return cases

	def printReport(self, report):
		for cases in report:
			print("    ", cases, '\t', end = ' ')

		print()

	def logHeaders(self, verbose):
		if (verbose):
			states = list(State)

			for state in states:
				print(state, '\t', end = ' ')

			print()
	
	def logReport(self, verbose):
		if (verbose):
				report = self.report()
				self.printReport(report)
	
	def simulation(self, generations, verbose):
		self.logHeaders(verbose)

		self.logReport(verbose)

		#self.logPopulation(self.population)

		for i in range(generations):
			self.nextGeneration()
			#self.logPopulation(self.population)
			self.logReport(verbose)
			if (i % 10 == 0):
				model.printImage(i)
	
	def numberOfDeaths(self):
		deaths = 0
		
		for line in self.population:
			for individual in line:
				if individual.state == State.dead:
					deaths = deaths + 1 
			
		return deaths

	def logPopulation(self, population):
		for i in range(len(population)):
			for j in range(len(population)):
				print(population[i][j].state.value, '\t', end = ' ')
			print()
		print()

	def printImage(self, name):

		lines = len(self.population)
		columns = len(self.population[0])
		t = (lines,columns,3)
		img = Image.new( mode = "RGB", size = (columns, lines))
		
		for i in range(lines):
		    for j in range(columns):
		    	if (self.population[i][j].state == State.healthy):
		    		img.putpixel((i, j), (0, 256, 0))   #Green
		    	elif (self.population[i][j].state == State.sick):
		    		img.putpixel((i, j), (256, 256, 0)) #Yellow
		    	elif (self.population[i][j].state == State.dead):
		    		img.putpixel((i, j), (256, 0, 0))   #Red
		    	elif (self.population[i][j].state == State.hospital):
		    		img.putpixel((i, j), (0, 0, 0))
		    	else:
		    		print("INVALID STATE")

		img.save("gen" + str(name) + ".png")
		#img.show()

numberOfRuns = 1
gridSize = 346
numberOfGenerations = 365


for i in range(0, numberOfRuns):
	model = RandomWalkModel(gridSize)
	model.simulation(numberOfGenerations, True)
	print(model.numberOfDeaths())
