import copy

class treeNode:
	totalNodes=0
	deepCopy=copy.deepcopy
	n=13 #number of cards
	
	def __init__(self, tableau, freeCells, foundation, parent):
		self.tableau=tableau
		self.freeCells=freeCells
		self.foundation=foundation
		self.parent=parent
		self.children=[]
		self.cardSetUp=self.createCardSetUp()
		self.bestFirstScore=self.calculateBestFirstSearchScore()
		self.AScore=self.calculateASearchScore()

		
		self.id=treeNode.totalNodes
		treeNode.totalNodes+=1

	def __repr__(self):
		return str(self.id)


	def checkFoundation(self):
		for aPile in self.foundation:
			if aPile and aPile[-1]['number']==treeNode.n-1:
				continue

			return False
		return True

	def cardSetUpAlreadyExists(self,aCardSetUp):
		return self.cardSetUp==aCardSetUp


	def expandNode(self):

		#first check if we can move any cards from the tableau piles
		
		for index,aPile in enumerate(self.tableau):
			if aPile:

				aCard=aPile[-1]
				result=self.moveToAFoundation(aCard,index,'t') #if a card can be moved to a foudation pile, then there is no point of trying other combinations
				
				if result:
					continue
				
				self.moveToAPile(aCard,index,'t')
				self.moveToAFreeCell(aCard,index,'t')

		#now check if we can move any cards from the freecells back to the tableau or to the foundation
		
		for index,aFreeCell in enumerate(self.freeCells):
			if aFreeCell:
				aCard=aFreeCell
				result=self.moveToAFoundation(aCard,index,'f')
				
				if result:
					continue
				
				self.moveToAPile(aCard,index,'f')

	def moveToAPile(self,card,cardOriginIndex,origin):
		
		for index,aPile in enumerate(self.tableau):
			if not aPile or (aPile[-1]['color']!=card['color'] and aPile[-1]['number']==card['number']+1):
				#pile is available when it is empty or the card on top of the pile has a different color and a value greater by one
				
				childFreeCells,childFoundation,childTableau=self.newInstance()
				childTableau[index].append(treeNode.deepCopy(card)) #add it to the new pile
				
				if origin=='t':
					childTableau[cardOriginIndex].pop() #remove card from its original pile
				else:
					childFreeCells[cardOriginIndex]=None #remove from free cell
				
				
				child=treeNode(childTableau,childFreeCells,childFoundation,self)
				self.children.append(child)
				return 1
		return 0
	
	def moveToAFreeCell(self,card,cardOriginIndex,origin):
		
		for index,aFreeCell in enumerate(self.freeCells):
			if not aFreeCell:
				childFreeCells,childFoundation,childTableau=self.newInstance()
				childFreeCells[index]=treeNode.deepCopy(card)

				childTableau[cardOriginIndex].pop() #remove card from its original pile
				
				child=treeNode(childTableau,childFreeCells,childFoundation,self)
				self.children.append(child)
				return 1
		return 0

	def moveToAFoundation(self,card,cardOriginIndex,origin):
		for index, aFoundation in enumerate(self.foundation):
			if (aFoundation[0]['number']==-1 and card['number']==0) or (aFoundation[-1]['symbol']==card['symbol'] and aFoundation[-1]['number']==card['number']-1):
		
				childFreeCells,childFoundation,childTableau=self.newInstance()
				
				if aFoundation[0]['number']==-1:
					childFoundation[index][0]=treeNode.deepCopy(card)
				else:
					childFoundation[index].append(treeNode.deepCopy(card))
				
				if origin=='t':
					childTableau[cardOriginIndex].pop() #remove card from its original pile
				else:
					childFreeCells[cardOriginIndex]=None #remove from its free cell
			

				child=treeNode(childTableau,childFreeCells,childFoundation,self)

				
				self.children.append(child)
				return 1

		return 0

	def createCardSetUp(self):
		#Joined string of the node's set up of the cards: free cells + foundation piles + tableau piles

		freeCellsJoin=''.join(aFreeCell['content'] if aFreeCell else str('none') for aFreeCell in self.freeCells)
		
		foundationJoin=''
		for aFoundation in self.foundation:
			if aFoundation[0]['number']!=-1:
				fj=''.join(aCard['content'] for aCard in aFoundation)
			else:
				fj='none'

			foundationJoin+=fj #memmory costly, needs to be fixed

		tableauJoin=''
		for aPile in self.tableau:
			if aPile:
				tj=''.join(aCard['content'] for aCard in aPile)
			else:
				tj='none'

			tableauJoin+=tj

		return freeCellsJoin+foundationJoin+tableauJoin
	
	def printFoundation(self): #prints top card of each pile in the foundation
		print([aPile[-1]['content']for aPile in self.foundation])

	def newInstance(self):
		return treeNode.deepCopy(self.freeCells),treeNode.deepCopy(self.foundation),treeNode.deepCopy(self.tableau)

		
	def calculateBestFirstSearchScore(self):
		#heuristic function:
		#the more cards in the foundation and the greater the average number of cards per foundation pile -> the less moves required to reach goal
		
		totalF,totalT,totalFoundationPiles=0,0,0

		for aPile in self.foundation:
			if aPile and aPile[0]['number']!=-1:
				totalF+=len(aPile)
				totalFoundationPiles+=1

		for aPile in self.tableau:
			totalT+=len(aPile)

		totalFC=sum(1 for aCard in self.freeCells if aCard)
		
		return totalT+totalFC-totalF-totalFoundationPiles-(totalF/4)

	def calculateASearchScore(self):

		currentNode,depth=self,0
		while currentNode.parent:
			depth+=1
			currentNode=currentNode.parent
		
		return self.bestFirstScore+depth