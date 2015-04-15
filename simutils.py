# Public imports
from random import uniform
import pygal

# Private imports
from basicutils import *
from supergraphs import *

# Constants
SIR_SUSCEPTIBLE = 0
SIR_INFECTED = 1
SIR_RECOVERED = 2
SIR_COLORS = ["deeppink3", "forestgreen", "goldenrod1"]

IC_UNKNOWING = 0
IC_INFORMED = 1
IC_COLORS = ["floralwhite", "dodgerblue4"]

def doSIRSimulation(g, infectionVector, q, r, maxSteps = 1000, animate = False, chartFile = ""):
	assert g.getNodeAmount() == len(infectionVector)
	assert 0 <= q <= 1
	assert 0 <= r <= 1

	iv = infectionVector[:]
	ivNext = [-1] * len(iv)
	stats = []

	if animate:
		colors = [SIR_COLORS[x] for x in iv]
		g.dumpToFile("{}.dot".format(nextFrame()), colors)
	
	for t in range(maxSteps):
		susceptibleAtT = sum([1 for i in iv if i == SIR_SUSCEPTIBLE])
		infectedAtT = sum([1 for i in iv if i == SIR_INFECTED])
		stats.append((susceptibleAtT, infectedAtT))

		if infectedAtT == 0:
			break;

		for i, v in enumerate(iv):
			if v == SIR_SUSCEPTIBLE:
				if ivNext[i] == -1:
					ivNext[i] = SIR_SUSCEPTIBLE
			elif v == SIR_INFECTED:
				if uniform(0, 1) <= r:
					ivNext[i] = SIR_RECOVERED
				else:
					ivNext[i] = SIR_INFECTED
					neighbours = g.getNeighbours(i)
					for n in neighbours:
						if iv[n] == SIR_SUSCEPTIBLE and uniform(0, 1) <= q:
							ivNext[n] = SIR_INFECTED
			elif v == SIR_RECOVERED:
				ivNext[i] = v

		iv = ivNext[:]
		ivNext = [-1] * len(iv)

		if animate: 
			colors = [SIR_COLORS[x] for x in iv]
			g.dumpToFile("{}.dot".format(nextFrame()), colors)
	
	if chartFile != "":
		amountInitiallyInfected = sum([1 for v in infectionVector if v == SIR_INFECTED])
		peakInfectionAmount = -1
		peakInfectionT = -1
		for t, (s, i) in enumerate(stats):
			if i > peakInfectionAmount:
				peakInfectionAmount = i
				peakInfectionT = t

		chart = pygal.Line(x_title="Timestep", y_title="Number of nodes", show_dots=False, x_labels_major_every=len(stats)//8, show_minor_x_labels=False, truncate_label=9999, style=pygal.style.LightStyle)
		chart.title = "SIR model({}, {}). Infected {} nodes. Peak infection time: {}. Infection duration: {}".format(q, r, amountInitiallyInfected, peakInfectionT, len(result))
		chart.x_labels = map(str, range(len(result)))
		chart.add("Susceptible", [p[0] for p in stats])
		chart.add("Infected", [p[1] for p in stats])
		chart.add("Recovered", [g.getNodeAmount() - p[0] - p[1] for p in stats])
	
		chart.render_to_file(chartFile)

	return stats

def doSIRTopNInfectedSimulation(g, amountOfPatients, q, r, chartFile = "", maxSteps = 10000, animate = False):
	assert g.getNodeAmount() > 0
	assert 0 <= amountOfPatients < g.getNodeAmount()
	assert maxSteps > 0

	iv = [SIR_SUSCEPTIBLE] * g.getNodeAmount()
	for p in g.getDegreeSortedNodes()[::-1][0:amountOfPatients]:
		iv[p] = SIR_INFECTED;

	result = doSIRSimulation(g, iv, q, r, maxSteps, animate = animate)
	infectionAmount = [t[1] for t in result]
	peakInfectionT = infectionAmount.index(max(infectionAmount))

	if chartFile != "":
		chart = pygal.Line(x_title="Timestep", y_title="Number of nodes", show_dots=False, x_labels_major_every=len(result)//8, show_minor_x_labels=False, truncate_label=9999, style=pygal.style.LightStyle)
		chart.title = "SIR model({}, {}). Infected top {} nodes. Peak infection time: {}. Infection duration: {}".format(q, r, amountOfPatients, peakInfectionT, len(result))
		chart.x_labels = map(str, range(len(result)))
		chart.add("Susceptible", [p[0] for p in result])
		chart.add("Infected", [p[1] for p in result])
		chart.add("Recovered", [g.getNodeAmount() - p[0] - p[1] for p in result])
	
		chart.render_to_file(chartFile)
	
	return result

def doSIRSeries(fG, fiv, q, r, runs = 1000, chartFile = "", maxSteps = 10000):
	g = fG()
	iv = fiv(g)

	assert len(iv) == g.getNodeAmount()
	assert runs > 0
	assert maxSteps > 0

	totalLength = 0
	totalPeakInfectionT = 0
	avgInfectionTrend = [0]
	avgSusceptibleTrend = [0]
	totalMaxInfected = -1;

	print("Started at: ", prettyNow())
	start = time()

	for i in range(runs):
		g = fG()
		iv = fiv(g)

		result = doSIRSimulation(g, iv, q, r, maxSteps)

		totalLength += len(result)
		infectionAmount = [t[1] for t in result]
		totalPeakInfectionT += infectionAmount.index(max(infectionAmount))
		totalMaxInfected += max(infectionAmount)

		if len(avgSusceptibleTrend) < len(result):
			diff = len(result) - len(avgSusceptibleTrend)
			avgSusceptibleTrend += [avgSusceptibleTrend[-1]] * diff
			avgInfectionTrend += [avgInfectionTrend[-1]] * diff

		for j, p in enumerate(result):
			avgSusceptibleTrend[j] += p[0]/runs
			avgInfectionTrend[j] += p[1]/runs

		if len(result) < len(avgSusceptibleTrend):
			lastSusceptibleVal = result[len(result) - 1][0]
			lastInfectedVal = result[len(result) - 1][1]

			for j in range(len(result), len(avgSusceptibleTrend)):
				avgSusceptibleTrend[j] += lastSusceptibleVal / runs
				avgInfectionTrend[j] += lastInfectedVal / runs

		#if i % 10 == 0:
		print("Iteration #", i)
	
	end = time()
	
	if chartFile != "":
		chart = pygal.Line(x_title="Timestep", y_title="Number of nodes", show_dots=False, x_labels_major_every=len(avgSusceptibleTrend)//8, show_minor_x_labels=False, truncate_label=9999, style=pygal.style.LightStyle)
		chart.title = "Average of {} simulations. SIR model({}, {}). {}. {}. Average peak infection time: {}. Average maximum infected: {}. Average infection duration: {}".format(runs, q, r, fG(""), fiv(""), totalPeakInfectionT//runs, totalMaxInfected//runs, totalLength//runs)
		chart.x_labels = map(str, range(len(avgInfectionTrend)))
		chart.add("Susceptible", avgSusceptibleTrend)
		chart.add("Infected", avgInfectionTrend)
		chart.add("Recovered", [g.getNodeAmount() - avgSusceptibleTrend[i] - avgInfectionTrend[i] for i in range(len(avgSusceptibleTrend))])
	
		chart.render_to_file(chartFile)

	print("Ended at: ", prettyNow())
	print("Duration: ", int(end - start), " seconds")
	
	return (totalLength, totalPeakInfectionT, avgInfectionTrend, avgSusceptibleTrend)

def doICSimulation(g, informationVector, alpha, maxSteps = 1000, animate = False):
	assert g.getNodeAmount() == len(informationVector)
	assert 0 <= alpha <= 1

	iv = informationVector[:]
	ivPrevious = iv[:]
	ivNext = [-1] * len(informationVector)
	stats = []

	if animate:
		colors = [IC_COLORS[x] for x in iv]
		g.dumpToFile("{}.dot".format(nextFrame()), colors)

	for t in range(maxSteps):
		amountInformed = sum([1 for x in iv if x == IC_INFORMED])
		stats.append(amountInformed)

		for i, v in enumerate(iv):
			if v == IC_UNKNOWING:
				informedNeighboursFrac = sum([1 for n in g.getNeighbours(i) if iv[n] == IC_INFORMED]) / max(1, g.getNeighbourCount(i))
				if informedNeighboursFrac >= alpha:
					ivNext[i] = IC_INFORMED
				else:
					ivNext[i] = IC_UNKNOWING
			elif v == IC_INFORMED:
				ivNext[i] = IC_INFORMED
				pass

		ivPrevious = iv
		iv = ivNext
		ivNext = [-1] * len(iv)

		if animate:
			colors = [IC_COLORS[x] for x in iv]
			g.dumpToFile("{}.dot".format(nextFrame()), colors)

		if iv == ivPrevious:
			break;
		
	return stats

def doICTopNInfectionSimulation(g, amountOfPatients, alpha, maxSteps = 1000, chartFile = "", animate = False):
	assert g.getNodeAmount() >= amountOfPatients
	assert 0 <= alpha <= 1
	assert maxSteps > 0

	iv = [IC_UNKNOWING] * g.getNodeAmount()
	for v in g.getDegreeSortedNodes()[::-1][0:amountOfPatients]:
		iv[v] = IC_INFORMED

	result = doICSimulation(g, iv, alpha, maxSteps, animate = animate)

	if chartFile != "":
		chart = pygal.Line(x_title="Timestep", y_title="Number of nodes", show_dots=False, x_labels_major_every=len(result)//8, show_minor_x_labels=False, truncate_label=9999, style=pygal.style.LightStyle)
		chart.title = "Information Cascade model({}). Top {} infection. Infection duration: {}. Final information coverage: {}%.".format(alpha, amountOfPatients, len(result), int(result[-1]/g.getNodeAmount()*100))
		chart.x_labels = map(str, range(len(result)))
		chart.add("Informed", result)
	
		chart.render_to_file(chartFile)

	return result

def doICSeries(fG, fiv, alpha, runs = 1000, chartFile = "", maxSteps = 10000):
	g = fG()
	iv = fiv(g)

	assert len(iv) == g.getNodeAmount()
	assert runs > 0
	assert maxSteps > 0
	assert 0 <= alpha <= 1

	totalLength = 0
	avgInformedTrend = [0]
	totalMaxInformed = 0
	maxInformed = 0

	print("Started at: ", prettyNow())
	start = time()

	for i in range(runs):
		g = fG()
		iv = fiv(g)

		result = doICSimulation(g, iv, alpha, maxSteps)

		totalLength += len(result)
		informedAmount = result[-1]
		maxInformed = max(maxInformed, informedAmount)
		totalMaxInformed += informedAmount

		if len(avgInformedTrend) < len(result):
			diff = len(result) - len(avgInformedTrend)
			avgInformedTrend += [avgInformedTrend[-1]] * diff

		for j, k in enumerate(result):
			avgInformedTrend[j] += k/runs

		if len(result) < len(avgInformedTrend):
			lastInformedVal = result[-1]

			for j in range(len(result), len(avgInformedTrend)):
				avgInformedTrend[j] += lastInformedVal / runs

		#if i % 10 == 0:
		print("Iteration #", i)
	
	end = time()
	
	if chartFile != "":
		chart = pygal.Line(x_title="Timestep", y_title="Number of nodes", show_dots=False, x_labels_major_every=len(avgInformedTrend)//8, show_minor_x_labels=False, truncate_label=9999, style=pygal.style.LightStyle)
		chart.title = "Average of {} simulations. IC model({}). {}. {}. Maximum informed: {}. Average maximum informed: {}. Average information duration: {}".format(runs, alpha, fG(""), fiv(""), maxInformed, totalMaxInformed//runs, totalLength//runs)
		chart.x_labels = map(str, range(len(avgInformedTrend)))
		chart.add("Informed", avgInformedTrend)
		chart.add("Uninformed", [g.getNodeAmount() - avgInformedTrend[i] for i in range(len(avgInformedTrend))])
	
		chart.render_to_file(chartFile)

	print("Ended at: ", prettyNow())
	print("Duration: ", int(end - start), " seconds")
	
	return (totalLength, maxInformed, totalMaxInformed, avgInformedTrend)
