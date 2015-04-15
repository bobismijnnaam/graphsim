# Public imports
from random import uniform, randrange, choice

# Private imports
from supergraphs import *
from basicutils import *

def makeCompleteGraph(size = 1, animate = False):
	assert size > 0

	g = Graph(size)
	if animate: g.dumpToFile("{}.dot".format(nextFrame()))

	for f in range(size):
		for s in range(f + 1, size):
			g.connect(f, s)
			if animate: g.dumpToFile("{}.dot".format(nextFrame()))

	return g

def makeRandomTreeGraph(size = 1, animate = False):
	assert size > 0

	g = Graph(size)
	if animate: g.dumpToFile("{}.dot".format(nextFrame()))

	for f in range(1, size):
		s = randrange(0, f)
		g.connect(f, s)
		if animate: g.dumpToFile("{}.dot".format(nextFrame()))
	
	return g

def makeERRandomGraph(size = 5, p = 0.5, animate = False):
	assert 0 <= p <= 1
	
	g = Graph(size)
	if animate: g.dumpToFile("{}.dot".format(nextFrame()))

	for f in range(size):
		for s in range(f + 1, size):
			if uniform(0, 1) <= p:
				g.connect(f, s)
				if animate: g.dumpToFile("{}.dot".format(nextFrame()))
	
	return g

def makePAMRandomGraph(initialGraph = Graph(1), nodesToAdd = 5, m = 1, animate = False):
	assert initialGraph.getNodeAmount() >= m > 0
	assert nodesToAdd > 0
	# assert initialGraph.isConnected() # Why did I add this?

	g = initialGraph.deepClone()
	if animate: g.dumpToFile("{}.dot".format(nextFrame()))

	choices = []
	for v in range(g.getNodeAmount()):
		choices += [v] * g.getNeighbourCount(v)
	
	# TODO
	if g.getNodeAmount() == 1:
		choices.append(0)

	for i in range(nodesToAdd):
		f = g.addNode();
		
		currentChoices = choices[:]
		
		for j in range(m):
			s = choice(currentChoices)
			currentChoices = [x for x in currentChoices if x != s]

			g.connect(f, s)
			if animate: g.dumpToFile("{}.dot".format(nextFrame()))
			choices.append(s)
			choices.append(f)

	return g
	
# TODO
def makeERRandomSquareGrid(w, h, p = 0.5):
	assert w <= h <= 2
	assert 0 <= p <= 1
	
	edges = []
	g = Graph(w * h)
	n = w * h

	# Almost all horizontal edges
	for y in range(h - 1):
		for x in range(w - 1):
			f = y * w + x
			s = y * w + x + 1
			edges.append(f, s)
	
	# Almost all vertical edges
	for y in range(h - 1):
		for x in range(w):
			f = y * w + x
			s = (y + 1) * w + x
			edges.append(f, s)

# TODO
def makeERRandomHexGrid(w, h, p = 0.5):
	pass

def makeCompletePAMGraph(completeSize = 3, nodesToAdd = 5, m = 1, animate = False):
	assert completeSize > 0
	assert nodesToAdd > 0
	assert m > 0

	return makePAMRandomGraph(makeCompleteGraph(completeSize, animate = animate), nodesToAdd, m, animate = animate)

def makeERPAMGraph(ERsize = 5, p = 0.5, nodesToAdd = 5, m = 1):
    assert ERsize > 0
    assert 0 <= p <= 1
    assert nodesToAdd > 0
    assert 0 < m <= ERsize

    return makePAMRandomGraph(makeERRandomGraph(ERsize, p), nodesToAdd, m)

# What do we want to know:
#	Portion unaffected, portion affected
#		Can be recorded by counting infected at every t?
#	Duration of presence of disease
#	Largest distance from patient 0
#	When was the peak in infections
