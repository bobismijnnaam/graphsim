# Public imports
from math import floor, log
from random import sample
from time import time
from datetime import datetime
import pygal

# Private imports
from supergraphs import *
from graphutils import *
from basicutils import *
from simutils import *

# Initial network: http://arxiv.org/pdf/1305.0205v1.pdf
# Takeaway: Initial degrees matter for the initial nodes (higher degrees => more links later on), but the distribution of the newly added node's degrees doesn't change

# TODO:
# Make simulations of SIS/SIR/Information Cascade

if __name__ == "__main__":
	# g = makeERRandomGraph(50, 0.05)
	# g = makeCompleteGraph(20)
	# g = makeCompletePAMGraph(10, 500, 3)
	# g = makeERRandomGraph(500, 2 * log(500)/500)
	# print(g.isConnected())
	# g.dumpToFile("ictest.dot")
	# g = makeCompleteGraph(5)
	# g = makeRandomTreeGraph(3)
	# g = makeCompleteGraph(3, animate = True)
	# g = makePAMRandomGraph(g, 50)
	# g = makeCompletePAMGraph(3, 50, 2 )
	# doSIRSingleInfectionSimulation(g, g.getMaxDegreeNode(), 0.15, 0.04, "movietest.svg", animate = True)
	# result = doInformationCascadeTopNInfectionSimulation(g, 3, 0.2, chartFile = "infocascade.svg")
	# resprint("Highest degree node", g.getMaxDegreeNode())
	# resprint("Max degree", g.getNeighbourCount(g.getMaxDegreeNode()))
	# resprint("Duration of simulation", len(result))

	# with open("graph.dot", "w") as f:
	# 	f.write(g.getDegreeColorFilledDOTRepresentation(True, True, "oranges5", 5))

	# doSIRSingleInfectionSeries(g, g.getMaxDegreeNode(), 0.001, 0.0001)
	
	# g = makeERPAMGraph(50, log(50)/50, 50, 1)
	# doSIRTopNInfectedSimulation(g, 1, 0.1, 0.05, chartFile = "simpleSIR.svg")
	# exit()

	# g = makeCompletePAMGraph(3, 50)
	# res = doSIRSingleInfectionSimulation(g, g.getMaxDegreeNode(), 0.01, 0.005, "mainresult.svg")

	########################################
	# Honours Simulation utility functions #
	########################################

	def fGGen(ker, kpam):
		def fg(p = None):
			if type(p) is str:
				return "ER({}, 2 * ln({})/{}) -> PAM({}, 1)".format(ker, ker, ker, kpam)
			else:
				return makeERPAMGraph(ker, 2 * log(ker)/ker, kpam, 1)

		return fg
	
	def randomlyChosen(k):
		def iv(g):
			if type(g) is str:
				return "{} random nodes infected first".format(k)
			else:
				iv = [SIR_SUSCEPTIBLE] * g.getNodeAmount()
				infected = sample(range(g.getNodeAmount()), k)
				for n in infected:
					iv[n] = SIR_INFECTED
				return iv

		return iv

	def topK(k):
		def iv(g):
			if type(g) is str:
				return "{} nodes with highest degree infected first".format(k) 
			else:
				iv = [SIR_SUSCEPTIBLE] * g.getNodeAmount()
				nodeDegrees = g.getDegreeSortedNodes()[::-1]
				for p in nodeDegrees[0:k]:
					iv[p] = SIR_INFECTED
				return iv
		
		return iv

	def genER(p = None):
		if type(p) is str:
			return "ER(100, 2 * ln(100) / 100)" 
		else:
			return makeERRandomGraph(100, 2 * log(100) / 100)

	def genPAM(p = None):
		if type(p) is str:
			return "PAM(100, 1)" 
		else:
			return makePAMRandomGraph(nodesToAdd = 100, m = 1)

	###################################
	# Honours Hypothesis 1 and 2 data #
	###################################

	for n in range(1, 3 + 1):
		doSIRSeries(fGGen(20, 50), randomlyChosen(n), 0.1, 0.05, chartFile="randomlyChosen_{}.svg".format(n), runs=500, maxSteps=10000)

	for n in range(1, 3 + 1):
		doSIRSeries(fGGen(20, 50), topK(n), 0.1, 0.05, chartFile="topK_{}.svg".format(n), runs=500, maxSteps=10000)

	###################################
	# Honours Hypothesis 3 and 4 data #
	###################################

	doSIRSeries(genPAM, topK(3), 0.1, 0.05, 500, "sir_pam_top3.svg")
	doSIRSeries(genPAM, randomlyChosen(3), 0.1, 0.05, 500, "sir_pam_random3.svg")
	doSIRSeries(genER, topK(3), 0.1, 0.05, 500, "sir_er_top3.svg")
	doSIRSeries(genER, randomlyChosen(3), 0.1, 0.05, 500, "sir_er_random3.svg")
	doICSeries(genPAM, topK(3), 0.2, 500, "ic_pam_top3.svg")
	doICSeries(genPAM, randomlyChosen(3), 0.2, 500, "ic_pam_random3.svg")
	doICSeries(genER, topK(3), 0.2, 500, "ic_er_top3.svg")
	doICSeries(genER, randomlyChosen(3), 0.2, 500, "ic_er_random3.svg")
