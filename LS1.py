import networkx as nx
import time


def LS1(graph, timeLimit, seed):
	print('LS1 local search ### method\n')
	startTime = time.time()
	timeNow = time.time() - startTime
	trace = []
	judge = 1
	k, coloredList, blankList = initialize_solution(graph)
	coloredSet = set(coloredList)
	blankSet = set(blankList)
	nodeRemovePerStep = 1
	iteration = 1
	removedNodes = []
	while (judge == 1) & (timeNow < timeLimit):
		trace.append(str(time.time() - startTime) + ',' + str(k))
		removedNodes = remove_nodes(graph, nodeRemovePerStep, coloredSet, blankSet)
		judge = local_search(graph, coloredSet, blankSet, iteration, seed, startTime, timeLimit)
		timeNow = time.time() - startTime
		k -= nodeRemovePerStep
		iteration += 1
	k += nodeRemovePerStep
	add_nodes(graph, removedNodes, coloredSet, blankSet)
	print('time spent on LS1 is %f s\n' %(time.time() - startTime))
	
	return coloredSet, trace

def initialize_solution(graph):
	coloredNode = 0
	coloredList = []
	nodeList = graph.nodes
	edgeList = graph.edges
	for i in nodeList:  # index of vertices [1, graph.number_of_nodes()]
		graph.nodes[i]['color'] = 'blank'
		graph.nodes[i]['edgeOtherSideNotColored'] = 0

	for anEdge in edgeList:
		if graph.nodes[anEdge[0]]['color'] == 'blank':
			graph.nodes[anEdge[0]]['color'] = 'colored'
			coloredNode += 1
			coloredList.append(anEdge[0])
	for anEdge in edgeList:
		if (graph.nodes[anEdge[0]]['color'] == 'colored') & (graph.nodes[anEdge[1]]['color'] == 'colored'):
			graph.edges[anEdge[0],anEdge[1]].update({'coloredEnd': 2})
		else:
			graph.edges[anEdge[0],anEdge[1]].update({'coloredEnd': 1})
			if graph.nodes[anEdge[0]]['color'] == 'colored':
				graph.nodes[anEdge[0]]['edgeOtherSideNotColored'] += 1
			else:
				graph.nodes[anEdge[1]]['edgeOtherSideNotColored'] += 1
	blankList = list(graph.nodes)
	for i in coloredList:
		blankList.remove(i)
	print('%d nodes are selected in initialization.\n' %coloredNode)
	return coloredNode, coloredList, blankList


def remove_nodes(graph, nodeDecStep, coloredSet, blankSet):
	removedNode = []
	for l in range(nodeDecStep):
		minNode = -1
		minEdgeOtherSideNotColored = graph.number_of_edges()
		for i in coloredSet:
			if graph.nodes[i]['edgeOtherSideNotColored'] <= minEdgeOtherSideNotColored:
				minNode = i
				minEdgeOtherSideNotColored = graph.nodes[i]['edgeOtherSideNotColored']
		removedNode.append(minNode)
		remove_a_node(graph, minNode, coloredSet, blankSet)
	return removedNode

def add_nodes(graph, nodesToBeAdded, coloredSet, blankSet):
	for i in nodesToBeAdded:
		add_a_node(graph, i, coloredSet, blankSet)

def remove_a_node(graph, removedNode, coloredSet, blankSet):
	graph.nodes[removedNode]['color'] = 'blank'
	for j in graph.adj[removedNode]:
		graph.nodes[j]['edgeOtherSideNotColored'] += 1
		if graph.nodes[j]['color'] == 'blank':
			graph.edges[removedNode, j].update({'coloredEnd': 0})
		else:
			graph.edges[removedNode, j].update({'coloredEnd': 1})
	coloredSet.remove(removedNode)
	blankSet.add(removedNode)

def add_a_node(graph, addedNode, coloredSet, blankSet):
	graph.nodes[addedNode]['color'] = 'colored'
	for j in graph.adj[addedNode]:
		graph.nodes[j]['edgeOtherSideNotColored'] -= 1
		if graph.nodes[j]['color'] == 'blank':
			graph.edges[addedNode, j].update({'coloredEnd': 1})
		else:
			graph.edges[addedNode, j].update({'coloredEnd': 2})
	coloredSet.add(addedNode)
	blankSet.remove(addedNode)
	
def local_search(graph, coloredSet, blankSet, iteration, seed, inputStartTime, inputTimeLimit):
	judge = 0
	edgeList = graph.edges.data()

	findSolution = 1

	minColoredNode = -1
	minEdgeOtherSideNotColored = graph.number_of_edges()
	for i in coloredSet:
		if graph.nodes[i]['edgeOtherSideNotColored'] <= minEdgeOtherSideNotColored:
			minColoredNode = i
			minEdgeOtherSideNotColored = graph.nodes[i]['edgeOtherSideNotColored']
	minColoredNodeList = []
	for i in coloredSet:
		if graph.nodes[i]['edgeOtherSideNotColored'] == minEdgeOtherSideNotColored:
			minColoredNodeList.append(i)
	# print('minColoredNodeList has %d nodes'%len(minColoredNodeList))
	maxBlankNode = 1
	maxEdgeOtherSideNotColored = -1
	for j in blankSet:
		if graph.nodes[j]['edgeOtherSideNotColored'] >= maxEdgeOtherSideNotColored:
			maxBlankNode = j
			maxEdgeOtherSideNotColored = graph.nodes[j]['edgeOtherSideNotColored']
	maxBlankNodeList = []
	for j in blankSet:
		if graph.nodes[j]['edgeOtherSideNotColored'] == maxEdgeOtherSideNotColored:
			maxBlankNodeList.append(j)
	# print('maxBlankNodeList has %d nodes'%len(maxBlankNodeList))

	count = 1
	timeNow = time.time() - inputStartTime

	while (judge == 0) & (timeNow < inputTimeLimit):
		pair = [minColoredNodeList[(count + seed)%len(minColoredNodeList)], maxBlankNodeList[(count*seed + iteration)%len(maxBlankNodeList)]]
		findSolution = 1
		pair0edgeOtherSideNotColored = graph.nodes[pair[0]]['edgeOtherSideNotColored']
		remove_a_node(graph, pair[0], coloredSet, blankSet)
		add_a_node(graph, pair[1], coloredSet, blankSet)
		for anEdge in edgeList:
			if anEdge[2]['coloredEnd'] == 0:  # an edge not covered, anEdge['coloredEnd'] == 0
				findSolution = 0
				add_a_node(graph, pair[0], coloredSet, blankSet)
				remove_a_node(graph, pair[1], coloredSet, blankSet)
				break
		count += 1
		if count%10 == 0:
			timeNow = time.time() - inputStartTime
		if findSolution == 1:
			# print('at %f, remove node %d, add node %d' %(time.time() - inputStartTime, pair[0], pair[1]))
			judge = 1
			return judge
	return judge

