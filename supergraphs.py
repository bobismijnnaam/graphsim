# Public imports

# Private imports

# Look ma, no imports!

class Graph:
	def __init__(self, n = 2):
		assert n > 0

		self._g = [[0 for x in range(n)] for x in range(n)]

	def addNode(self):
		for row in self._g:
			row.append(0);

		self._g.append([0 for x in range(len(self._g[0]))])

		return len(self._g) - 1
	
	def connect(self, n, m):
		assert n != m
		assert n < len(self._g)
		assert m < len(self._g)

		self._g[n][m] = 1
		self._g[m][n] = 1

	def getDOTRepresentation(self, complete = True, readable = False, includeNodeIDs = True, degreeAsLabel = True):
		result = ""

		if complete:
			result = "graph G {"
			if readable:
				result += "\n"

		for rowI in range(len(self._g)):
			for colI in range(rowI + 1, len(self._g)):
				if self._g[rowI][colI] == 1:
					if readable:
						result += "\t"

					result += "{} -- {};".format(rowI, colI)

					if readable:
						result += "\n"

		if includeNodeIDs or degreeAsLabels:
			for v in range(len(self._g)):
				if readable:
					result += "\t"

				if not degreeAsLabel:
					result += "{};".format(v)
				else:
					result += "{} [label = {}];".format(v, self.getNeighbourCount(v))

				if readable:
					result += "\n"

		if complete:
			result += "}"

		return result

	def dumpToFile(self, dotFile = "", colors = [], colorscheme = ""):
		result = ""

		if colors:
			if colorscheme != "":
				colors = ["/{}/{}".format(colorscheme, x) for x in colors]

			result = self.getColorFilledDOTRepresentation(colors)
		else:
			result = self.getDOTRepresentation()

		with open(dotFile, "w") as f:
			f.write(result)
	
	def getDegreeColorFilledDOTRepresentation(self, readable = False, degreeAsLabel = True, colorscheme = "__none__", colorMax = -1):
		maxNeighourCount = self.getMaxNeighbourCount() 

		if colorscheme == "__none__":
			colors = ['"{}{}"'.format('grey', floor(sum(row) / maxNeighourCount * 100)) for row in self._g]
		else:
			colors = ['"/{}/{}"'.format(colorscheme, 1 + floor(sum(row) / maxNeighourCount * (colorMax - 1))) for row in self._g]

		return self.getColorFilledDOTRepresentation(colors, degreeAsLabel, True)

	def getColorFilledDOTRepresentation(self, colors, degreeAsLabel = True, readable = False):
		result = "graph G {"
		if readable:
			result += "\n"

		result += self.getDOTRepresentation(False, readable, degreeAsLabel = True)

		for v, c in enumerate(colors):
			if readable:
				result += "\t"
			
			result += "{} [style = filled, fillcolor = {}];".format(v, c)

			if readable:
				result += "\n"

		result += "}"

		return result

	def getNodeAmount(self):
		return len(self._g)

	def getNeighbourCount(self, v):
		return sum(self._g[v])

	def getMaxNeighbourCount(self):
		return max([sum(row) for row in self._g])

	def getNeighbours(self, v):
		return [i for i, x in enumerate(self._g[v]) if x == 1]

	def getDegreeSortedNodes(self):
		nodes = [(v, self.getNeighbours(v)) for v in range(self.getNodeAmount())]
		nodes = sorted(nodes, key=lambda pair: pair[1])
		return [p[0] for p in nodes]

	def isConnected(self):
		assert len(self._g) > 0

		visited = [False] * len(self._g)
		toVisit = [0]

		while toVisit:
			currV = toVisit.pop()
			visited[currV] = True
			toVisit += [x for x in self.getNeighbours(currV) if not visited[x]]

		return sum(visited) == self.getNodeAmount()

	def getMaxDegreeNode(self):
		maxNode = -1
		maxDegree = -1
		for v in range(self.getNodeAmount()):
			if self.getNeighbourCount(v) > maxDegree:
				maxNode = v
				maxDegree = self.getNeighbourCount(v)
		
		return maxNode

	def deepClone(self):
		g = Graph(self.getNodeAmount())

		for f in range(self.getNodeAmount()):
			for s in range(f + 1, self.getNodeAmount()):
				if self._g[f][s] == 1:
					g.connect(f, s)

		return g
