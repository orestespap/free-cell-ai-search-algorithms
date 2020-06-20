import re
from searchLibrary import depthFirstSearch, breadthFirstSearch, bestFirstSearch, ASearch
from nodeClass import treeNode

def list_lines_txt(filename):
	with open(filename,'r') as afile:
		return [aline.replace('\n','') for aline in afile]

def constructTableau(table):
	for index,aSubTable in enumerate(table):
		table[index]=aSubTable.strip().split(' ')
	
	findPattern=re.findall
	for aSubTable in table:
		for index,aString in enumerate(aSubTable):
			
			aSubTable[index]={'symbol':aString[0],'number':int(findPattern(r"\d+", aString)[0]), 'content':aString}
			
			if aSubTable[index]['symbol'] in 'S C':
				aSubTable[index]['color']='black'
			else:
				aSubTable[index]['color']='red'
	return table

if __name__ == '__main__':

	options={1:depthFirstSearch, 2:breadthFirstSearch, 3:bestFirstSearch, 4:ASearch}
	while True:


		answer=int(input('Select search algorithm\n1.)Depth first\n2.)Breadth First\n3.)Best first\n4.)A*\nINPUT (1-4): '))
		if answer<1 or answer>4:
			print('Bye')
			break
		
		searchAlgorithm=options[answer]
		
		for i in range(7,11):
			print(f'Running test{i}...')
			table=list_lines_txt(f'test{i}.txt')
			
			tableau=constructTableau(table)
			freeCells,foundation=[None,None,None,None],[[],[],[],[]]

			for index,aColor in enumerate('SHDC'):
				foundation[index].append({'number':-1,'symbol':aColor,'content':f'-1{aColor}'})
			
			root=treeNode(tableau,freeCells,foundation,None)
			winner,seconds_=searchAlgorithm(root)
			if winner:
				print('Foundation:')
				winner.printFoundation()

				currentNode,numberOfMoves=winner,0
				while currentNode.parent:
					numberOfMoves+=1
					currentNode=currentNode.parent
				print(f'{seconds_} seconds to beat test {i}.\n{numberOfMoves} moves were made.')
			else:
				print(f'Failed to beat test {i} within time limit or all of the nodes were explored ...')