import time
sleepTime=30
numberOfLoops=10000
tl=100

def breadthFirstSearch(rootNode):
	print('Breadth First search ...')
	start=time.time()
	
	queue, visitedList, win, lap, goToSleep, timeLimit = [rootNode], [], False, time.time, time.sleep, tl
	
	appendToQueue=queue.append
	popFromQueue=queue.pop
	appendToVisitedList=visitedList.append

	timePassed=lap()-start
	loops=0
	while len(queue)>0 and timePassed<timeLimit:
		currentNode=queue[0]
		popFromQueue(0)
		appendToVisitedList(currentNode)

		currentNode.expandNode()

		for aChild in currentNode.children:
			
			if aChild.checkFoundation():
				timePassed=lap()-start
				return aChild,timePassed
			
			if not nodeAlreadyExists(visitedList,queue,aChild):
				appendToQueue(aChild)

		loops+=1
		
		if loops%numberOfLoops==0:
			print(f'Visited nodes: {len(visitedList)}\nNot visited nodes: {len(queue)}\nPC is now chilling for {sleepTime} seconds...')
			goToSleep(sleepTime)
			print('Back to work ...')
		
		timePassed=lap()-start
		
	return None,timePassed



def depthFirstSearch(rootNode):
	print('Depth First search ...')
	start=time.time()
	
	stack, visitedList, win, lap, goToSleep, timeLimit = [rootNode], [], False, time.time, time.sleep, tl
	
	appendToStack=stack.append
	popFromStack=stack.pop
	appendToVisitedList=visitedList.append

	timePassed=lap()-start
	loops=0
	while len(stack)>0 and timePassed<timeLimit:
		currentNode=stack[-1]
		popFromStack(-1)
		appendToVisitedList(currentNode)

		currentNode.expandNode()

		for aChild in currentNode.children:
			
			if aChild.checkFoundation():
				timePassed=lap()-start
				return aChild, timePassed
			
			if not nodeAlreadyExists(visitedList,stack,aChild):
				appendToStack(aChild)

		loops+=1
		
		if loops%numberOfLoops==0:
			print(f'Visited nodes: {len(visitedList)}\nNot visited nodes: {len(stack)}\nPC is now chilling for {sleepTime} seconds...')
			goToSleep(sleepTime)
			print('Back to work ...')
		
		timePassed=lap()-start
		
	return None,timePassed

def bestFirstSearch(rootNode):
	print('Best First search ...')
	start=time.time()
	
	notVisitedList, visitedList, win, lap, goToSleep, timeLimit = [rootNode], [], False, time.time, time.sleep, tl
	
	appendToNotVisitedList=notVisitedList.append
	popFromNotVisitedList=notVisitedList.pop
	appendToVisitedList=visitedList.append
	sortNotVisitedList=notVisitedList.sort


	timePassed=lap()-start
	loops=0
	
	while len(notVisitedList)>0 and timePassed<timeLimit:

		currentNode=notVisitedList[0]
		popFromNotVisitedList(0)
		appendToVisitedList(currentNode)
		
			
		if currentNode.checkFoundation():
			timePassed=lap()-start
			return currentNode,timePassed

		currentNode.expandNode()

		for aChild in currentNode.children:
			if not nodeAlreadyExists(visitedList,notVisitedList,aChild):
				appendToNotVisitedList(aChild)

		sortNotVisitedList(key= lambda aNode: aNode.bestFirstScore)

		loops+=1
		
		if loops%numberOfLoops==0:
			print(f'Visited nodes: {len(visitedList)}\nNot visited nodes: {len(notVisitedList)}\nPC is now chilling for {sleepTime} seconds...')
			goToSleep(sleepTime)
			print('Back to work ...')
		
		timePassed=lap()-start
		
	return None,timePassed


def ASearch(rootNode):
	print('A* search ...')
	start=time.time()
	
	notVisitedList, visitedList, win, lap, goToSleep, timeLimit = [rootNode], [], False, time.time, time.sleep, tl
	
	appendToNotVisitedList=notVisitedList.append
	popFromNotVisitedList=notVisitedList.pop
	appendToVisitedList=visitedList.append
	sortNotVisitedList=notVisitedList.sort


	timePassed=lap()-start
	loops=0
	
	while len(notVisitedList)>0 and timePassed<timeLimit:
		currentNode=notVisitedList[0]
		popFromNotVisitedList(0)
		appendToVisitedList(currentNode)
		
			
		if currentNode.checkFoundation():
			print('DONE!!!')
			timePassed=lap()-start
			return currentNode,timePassed

		currentNode.expandNode()

		for aChild in currentNode.children:
			if not nodeAlreadyExists(visitedList,notVisitedList,aChild):
				appendToNotVisitedList(aChild)

		sortNotVisitedList(key= lambda aNode: aNode.AScore)

		loops+=1
		
		if loops%numberOfLoops==0:
			print(f'Visited nodes: {len(visitedList)}\nNot visited nodes: {len(notVisitedList)}\nPC is now chilling for {sleepTime} seconds...')
			goToSleep(sleepTime)
			print('Back to work ...')
		
		timePassed=lap()-start
		
	return None,timePassed



def nodeAlreadyExists(visitedList,notVisitedList,nodeOfInterest):
#If newly generated node's state of the deck already exists in the graph, then the node is added to the unvisited node list IFF
#its score is lower (and therefore better) than the other node's score. If there are multiple visited/unvisited nodes with the same state of the deck
#but a higher score, then the new node is added to the unexplored nodes

	for aNode in visitedList: 
		if aNode.cardSetUpAlreadyExists(nodeOfInterest.cardSetUp) and aNode.AScore<nodeOfInterest.AScore:
			return True

	for aNode in notVisitedList:
		if aNode.cardSetUpAlreadyExists(nodeOfInterest.cardSetUp) and aNode.AScore<nodeOfInterest.AScore:
			return True
	
	return False
	


if __name__ == '__main__':
	pass