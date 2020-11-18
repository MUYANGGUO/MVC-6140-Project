import networkx as nx
import time
# import random
# from random import shuffle
# from itertools import combinations

def LS1(graph, timeLimit, seed):
	print('LS1 local search ### method\n')
	startTime = time.clock()
	timeNow = time.clock() - startTime
	judge = 1
	# k = graph.number_of_nodes()
	k, coloredList, blankList = initialize_solution(graph)
	# print(graph._node)
	# print(graph.edges.data())
	nodeRemovePerStep = 1
	iteration = 1
	removedNodes = []
	while (judge == 1) & (timeNow < timeLimit):
		removedNodes = remove_nodes(graph, nodeRemovePerStep, coloredList, blankList)
		print('nodes removed in iteration %d:' %iteration)
		for j in removedNodes:
			print(j)
		# print(graph._node)
		# print(graph.edges.data())
		judge = local_search(graph, coloredList, blankList, iteration, seed)
		timeNow = time.clock() - startTime
		print('judge is %d, timeNow is %f, timeLimit is %f' %(judge, timeNow, timeLimit))
		k -= nodeRemovePerStep
		iteration += 1
	add_nodes(graph, removedNodes, coloredList, blankList)
	print('final solution has %d colored nodes, they are listed below:' %len(coloredList))
	print(coloredList)
	# print(graph.edges.data())
	print('time spent on LS1 is %f s\n' %timeNow)

def initialize_solution(graph):
	coloredNode = 0
	coloredList = []
	edgeList = graph.edges
	for i in range(1, graph.number_of_nodes() + 1):  # index of vertices [1, graph.number_of_nodes()]
		graph.node[i]['color'] = 'blank'
		graph.node[i]['edgeOtherSideNotColored'] = 0

	for anEdge in edgeList:
		if graph.node[anEdge[0]]['color'] == 'blank':
			graph.node[anEdge[0]]['color'] = 'colored'
			coloredNode += 1
			coloredList.append(anEdge[0])
	for anEdge in edgeList:
		if (graph.node[anEdge[0]]['color'] == 'colored') & (graph.node[anEdge[1]]['color'] == 'colored'):
			graph.edges[anEdge[0],anEdge[1]].update({'coloredEnd': 2})
		else:
			graph.edges[anEdge[0],anEdge[1]].update({'coloredEnd': 1})
			if graph.node[anEdge[0]]['color'] == 'colored':
				graph.node[anEdge[0]]['edgeOtherSideNotColored'] += 1
			else:
				graph.node[anEdge[1]]['edgeOtherSideNotColored'] += 1
	blankList = [x for x in range(1, graph.number_of_nodes() + 1)]
	for i in coloredList:
		blankList.remove(i)
	print('%d nodes are selected in initialization.\n' %coloredNode)
	return coloredNode, coloredList, blankList


def remove_nodes(graph, nodeDecStep, coloredList, blankList):
	removedNode = []
	for l in range(nodeDecStep):
		minNode = -1
		minEdgeOtherSideNotColored = graph.number_of_edges()
		for i in coloredList:
			if graph.node[i]['edgeOtherSideNotColored'] <= minEdgeOtherSideNotColored:
				minNode = i
				minEdgeOtherSideNotColored = graph.node[i]['edgeOtherSideNotColored']
		removedNode.append(minNode)
		remove_a_node(graph, minNode, coloredList, blankList)
	return removedNode

def add_nodes(graph, nodesToBeAdded, coloredList, blankList):
	for i in nodesToBeAdded:
		add_a_node(graph, i, coloredList, blankList)

def remove_a_node(graph, removedNode, coloredList, blankList):
	graph.node[removedNode]['color'] = 'blank'
	for j in graph.adj[removedNode]:
		graph.node[j]['edgeOtherSideNotColored'] += 1
		if graph.node[j]['color'] == 'blank':
			graph.edges[removedNode, j].update({'coloredEnd': 0})
		else:
			graph.edges[removedNode, j].update({'coloredEnd': 1})
	coloredList.remove(removedNode)
	blankList.append(removedNode)

def add_a_node(graph, addedNode, coloredList, blankList):
	graph.node[addedNode]['color'] = 'colored'
	for j in graph.adj[addedNode]:
		graph.node[j]['edgeOtherSideNotColored'] -= 1
		if graph.node[j]['color'] == 'blank':
			graph.edges[addedNode, j].update({'coloredEnd': 1})
		else:
			graph.edges[addedNode, j].update({'coloredEnd': 2})
	coloredList.append(addedNode)
	blankList.remove(addedNode)
	
def local_search(graph, coloredList, blankList, iteration, seed):
	judge = 0
	edgeList = graph.edges.data()

	findSolution = 1

	allMovingPairs = []
	minNode = -1
	minEdgeOtherSideNotColored = graph.number_of_edges()
	for i in coloredList:
		if graph.node[i]['edgeOtherSideNotColored'] <= minEdgeOtherSideNotColored:
			minNode = i
			minEdgeOtherSideNotColored = graph.node[i]['edgeOtherSideNotColored']
	minNodeList = []
	for i in coloredList:
		if graph.node[i]['edgeOtherSideNotColored'] == minEdgeOtherSideNotColored:
			minNodeList.append(i)
	print('minNodeList has %d nodes'%len(minNodeList))

	count = 1
	while (judge == 0) & (count <= len(blankList)):
		pair = [minNodeList[count%len(minNodeList)], blankList[(count*seed + 3 + iteration)%len(blankList)]]
		print('(count*(seed + 1) + 3 + iteration) is %d'%(count*(seed + 1) + 3 + iteration))
		findSolution = 1
		pair0edgeOtherSideNotColored = graph.node[pair[0]]['edgeOtherSideNotColored']
		remove_a_node(graph, pair[0], coloredList, blankList)
		add_a_node(graph, pair[1], coloredList, blankList)
		for anEdge in edgeList:
			if anEdge[2]['coloredEnd'] == 0:  # an edge not covered, anEdge['coloredEnd'] == 0
				findSolution = 0
				add_a_node(graph, pair[0], coloredList, blankList)
				remove_a_node(graph, pair[1], coloredList, blankList)
				break
		count += 1
		if findSolution == 1:
			print('remove node %d, add node %d' %(pair[0], pair[1]))
			judge = 1
			return judge
	return judge

