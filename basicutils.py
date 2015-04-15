# Public imports
from time import time
from datetime import datetime

def partialShuffle(l, partSize):
	currPos = 0;

	while currPos < partSize:
		t = randrange(currPos, len(l))
		l[currPos], l[t] = l[t], l[currPos]
		currPos += 1

def prettyNow():
	ts = time()
	return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

currentFrame = 0
def nextFrame():
	global currentFrame

	nf = currentFrame
	currentFrame += 1
	return nf
