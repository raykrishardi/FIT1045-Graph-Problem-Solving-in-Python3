# Import the required functions from the graphFileOps.py, intersection.py, union.py, supergraph.py, and connectivity.py file
from graphFileOps import getVerticesFromFile, getAdjacencyMatrixFromFile, writeMatrixToFile, getIndex, getElementAtIndex, popElementAtIndex
from intersection import getIntersectVertices, getAdjacencyMatrix
from union import getUnionVertices, initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection, initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight
from supergraph import getSupergraphValidIntersectEdges, checkSwapGraphsAndGetIntermediateGraphExistFlag
from connectivity import writeLineToFile, writeConnectivityToFile

# Function that returns the index of the next cheapest vertex
def getNextCheapestVertexIndex(vertices, visited, startVertices):
    # Initialise the default value to -1 because 0 is a valid index
    # Because vertex at index 0 might have weight of 0 which is the smallest but invalid
    minVertexIndex = -1

    # Loop through each vertices
    for i in range(len(vertices)):
        # If there is a vertex that has an edge (weight is not equal to 0) and that vertex has not been visited before and
        # the vertex is not one of the start vertices then assume that vertex index has the smallest weight and exit the loop
        if vertices[i] != 0 and (not visited[i]) and i not in startVertices:
            minVertexIndex = i
            break

    # Loop through each vertices
    for i in range(len(vertices)):
        # If there is another vertex that has an edge (weight is not equal to 0) and
        # that vertex has weight smaller than the vertex that is assumed to have the smallest weight
        # and that vertex has not been visited before and
        # that vertex is not one of the start vertices then assume that vertex index has the smallest weight
        if vertices[i] != 0 and vertices[i] < vertices[minVertexIndex] and (not visited[i]) and i not in startVertices:
            minVertexIndex = i

    return minVertexIndex

# Function that returns the index of the cheapest path cost
def getCheapestCostIndex(costs):
    minCostIndex = 0

    # Loop through each path costs and get the index of the path with the smallest cost
    for i in range(1, len(costs)):
        if costs[i] < costs[minCostIndex]:
            minCostIndex = i

    return minCostIndex

# Function that returns the cheapest path
def getCheapestPath(startVertices, stopVertices, intermediateVertices, intermediateAdjacencyMatrix, graphOutputFileName):
    paths = []
    costs = []

    # Initialise the start vertices with the index of each start vertices in the intermediate vertices
    for i in range(len(startVertices)):
        startVertices[i] = getIndex(intermediateVertices, startVertices[i])

    # Initialise the stop vertices with the index of each stop vertices in the intermediate vertices
    for i in range(len(stopVertices)):
        stopVertices[i] = getIndex(intermediateVertices, stopVertices[i])

    # Loop through each start vertices
    for i in range(len(startVertices)):
        # Queue of vertices to be processed/served
        verticesQueue = []

        # List that represents whether a particular vertex has been visited or not
        visited = [False] * len(intermediateVertices)

        # Reset the path cost to 0 for each iteration
        cost = 0

        # Get the start vertex index from the start vertices
        startVertexIndex = startVertices[i]

        # Append the start vertex index to the queue
        # In addition, indicate that the vertex specified by the start vertex index has been visited
        # as the vertex is already in the queue to be processed
        verticesQueue.append(startVertexIndex)
        visited[startVertexIndex] = True

        # Get the path for each starting vertices
        paths.append([intermediateVertices[startVertexIndex]])

        # Keep looping until the next vertex index to be processed is in the stop vertices
        while verticesQueue[0] not in stopVertices:
            vertexIndex = getElementAtIndex(verticesQueue, 0)  # Get the index of the vertex to be processed
            verticesQueue = popElementAtIndex(verticesQueue, 0)  # Pop the queue at index 0

            # Get the index of the next cheapest adjacent vertex
            nextCheapestVertexIndex = getNextCheapestVertexIndex(intermediateAdjacencyMatrix[vertexIndex], visited, startVertices)

            # Increment the cost with the weight of the next cheapest adjacent vertex accordingly
            cost += intermediateAdjacencyMatrix[vertexIndex][nextCheapestVertexIndex]

            # Append the index of the next cheapest adjacent vertex to the queue
            # In addition, indicate that the vertex has been visited
            # as the vertex is already in the queue to be processed
            verticesQueue.append(nextCheapestVertexIndex)
            visited[nextCheapestVertexIndex] = True

            # Append the path with the next cheapest adjacent vertex accordingly
            paths[i].append(intermediateVertices[nextCheapestVertexIndex])

        # Append the total cost accordingly
        costs.append(cost)

    # Get path with the cheapest cost and write the cheapest cost to the appropriate file
    pathIndexWithSmallestCost = getCheapestCostIndex(costs)
    writeLineToFile(graphOutputFileName[:len(graphOutputFileName)-4] + "pathCost.txt", str(costs[pathIndexWithSmallestCost]))

    return paths[pathIndexWithSmallestCost]

# Function that sorts the selected intermediate vertices in alphabetical order using selection sort
def sortSelectedIntermediateVertices(selectedIntermediateVertices):
    for i in range(len(selectedIntermediateVertices)):
        least = i
        for j in range(i+1, len(selectedIntermediateVertices)):
            if selectedIntermediateVertices[j] < selectedIntermediateVertices[least]:
                least = j
        tmp = selectedIntermediateVertices[least]
        selectedIntermediateVertices[least] = selectedIntermediateVertices[i]
        selectedIntermediateVertices[i] = tmp

# Function that initialises the greedy vertices and adjacency matrix with cheapest path
def initialiseGreedyAdjacencyMatrixWithCheapestPath(intermediateVertices, intermediateAdjacencyMatrix, cheapestPath, vertices1, greedyVertices, greedyAdjMatrix):
    # Get the intermediate vertices from the cheapest path without the first and last element of the cheapest path
    # This is because the the first and last vertices are already in greedy vertices and adjacency matrix
    selectedIntermediateVertices = cheapestPath[1:-1]

    # Sort the selected intermediate vertices in alphabetical order
    sortSelectedIntermediateVertices(selectedIntermediateVertices)

    # Additional counter for the selected intermediate vertices
    # This is because the for loop index is already used for inserting the new intermediate vertices to the existing greedy vertices
    selectedIntermediateVerticesCounter = 0

    # Insert the new intermediate vertices to the greedy vertices starting as the next element of vertices 1
    for i in range(len(vertices1), len(vertices1)+len(selectedIntermediateVertices)):
        greedyVertices.insert(i, selectedIntermediateVertices[selectedIntermediateVerticesCounter])
        selectedIntermediateVerticesCounter += 1

    # Insert the weight of the new intermediate vertices to the greedy adjacency matrix starting as the next element of vertices 1
    # (weight is initialised to 0)
    for vertex in greedyAdjMatrix:
        for i in range(len(vertices1), len(vertices1) + len(selectedIntermediateVertices)):
            vertex.insert(i, 0)

    # Insert the row for the new intermediate vertices in the greedy adjacency matrix starting as the next element of vertices 1
    for i in range(len(vertices1), len(vertices1) + len(selectedIntermediateVertices)):
        greedyAdjMatrix.insert(i, [0] * len(greedyVertices))

    # Initialise the greedy adjacency matrix with the cheapest path weight
    for i in range(len(cheapestPath)-1):
        # Get the index of the cheapest path vertices in intermediate vertices
        vertex1IndexInVertices2 = getIndex(intermediateVertices, cheapestPath[i])
        vertex2IndexInVertices2 = getIndex(intermediateVertices, cheapestPath[i + 1])

        # Get the index of the cheapest path vertices in greedy vertices
        vertex1IndexInGreedyVertices = getIndex(greedyVertices, cheapestPath[i])
        vertex2IndexInGreedyVertices = getIndex(greedyVertices, cheapestPath[i + 1])

        # Get the weight from the intermediate adjacency matrix
        weight = intermediateAdjacencyMatrix[vertex1IndexInVertices2][vertex2IndexInVertices2]

        # Assign weight to the greedy adjacency matrix
        greedyAdjMatrix[vertex1IndexInGreedyVertices][vertex2IndexInGreedyVertices] = weight
        greedyAdjMatrix[vertex2IndexInGreedyVertices][vertex1IndexInGreedyVertices] = weight

# Function that writes the greedy adjacency matrix and vertices to a file with the appropriate formatting
def writeGreedyAdjacencyMatrixToFile(vertices1, vertices2, vertices3, adjacencyMatrix1, adjacencyMatrix2, adjacencyMatrix3, fileName1, fileName2, fileName3):
    # Represent the vertices, adjacency matrix, and file names of the 3 input graphs
    graphs = [
        [vertices1, adjacencyMatrix1, fileName1],
        [vertices2, adjacencyMatrix2, fileName2],
        [vertices3, adjacencyMatrix3, fileName3]
    ]

    # Check when to perform graph swapping to make sure that the intermediate graph occupies the middle section
    # and get the appropriate flag that indicates whether an intermediate graph exist or not
    intermediateGraphExist = checkSwapGraphsAndGetIntermediateGraphExistFlag(graphs)

    # Assign the appropriate vertices, adjacency matrix, and file names with the intermediate graph in the middle section
    # In this case, if there is no intermediate graph, the graphs will be listed in the order received as no swapping of graphs will occur
    vertices1 = graphs[0][0]
    vertices2 = graphs[1][0]
    vertices3 = graphs[2][0]

    adjacencyMatrix1 = graphs[0][1]
    adjacencyMatrix2 = graphs[1][1]
    adjacencyMatrix3 = graphs[2][1]

    fileName1 = graphs[0][2]
    fileName2 = graphs[1][2]
    fileName3 = graphs[2][2]

    # Generate the output file name
    # This is done by removing the ".txt" extension from the file names and concatenate the required additional string
    # with the file names with a new .txt extension at the end of it
    graphOutputFileName = "greedy" + fileName1[:len(fileName1)-4] + fileName2[:len(fileName2)-4] + fileName3[:len(fileName3)-4] + ".txt"

    # Get the greedy vertices and adjacency matrix which contains all vertices in vertices 1 and 3
    greedyVertices = getUnionVertices(vertices1, vertices3)
    greedyAdjMatrix = getAdjacencyMatrix(greedyVertices)

    # Check whether an intermediate graph exist or not
    if intermediateGraphExist:
        # Get the intersect edges between vertices 1 and 2 and vertices 3 and 2
        validIntersectEdges1 = getSupergraphValidIntersectEdges(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
        validIntersectEdges2 = getSupergraphValidIntersectEdges(vertices3, vertices2, adjacencyMatrix3, adjacencyMatrix2)

        # Initialise the greedy adjacency matrix with adjacency matrix 1 and 3's weights while excluding weights from
        # intersect edges (intersect of vertices 1 and 2 and vertices 3 and 2)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices1, adjacencyMatrix1, validIntersectEdges1, validIntersectEdges2, [], greedyVertices, greedyAdjMatrix)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices3, adjacencyMatrix3, validIntersectEdges1, validIntersectEdges2, [], greedyVertices, greedyAdjMatrix)

        # Initialise the greedy adjacency matrix with smallest weight from adjacency matrix 1 or 2 and
        # adjacency matrix 3 or 2 by using the intersect edges (intersect of vertices 1 and 2 and vertices 3 and 2)
        # This is achieved by comparing the weight in adjacency matrix 1, 2, and 3 that correlates with the intersect edges
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges1, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, greedyVertices, greedyAdjMatrix)
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges2, vertices3, vertices2, adjacencyMatrix3, adjacencyMatrix2, greedyVertices, greedyAdjMatrix)

        # Initialise the intermediate adjacency matrix (adjacencyMatrix2) with smallest weight from adjacency matrix 1 or 2 and
        # adjacency matrix 3 or 2 by using the intersect edges (intersect of vertices 1 and 2 and vertices 3 and 2)
        # This is achieved by comparing the weight in adjacency matrix 1, 2, and 3 that correlates with the intersect edges
        # This is because we need to update the weight in intermediate graph to smaller weights for finding the cheapest connection
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges1, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, vertices2, adjacencyMatrix2)
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges2, vertices3, vertices2, adjacencyMatrix3, adjacencyMatrix2, vertices2, adjacencyMatrix2)

        # Get the intersect vertices between vertices 1 and 2 (start vertices) and vertices 3 and 2 (stop vertices)
        startVertices = getIntersectVertices(vertices1, vertices2)
        stopVertices = getIntersectVertices(vertices3, vertices2)

        # Get the cheapest path
        cheapestPath = getCheapestPath(startVertices, stopVertices, vertices2, adjacencyMatrix2, graphOutputFileName)

        # Initialise the greedy adjacency matrix with the cheapest path
        initialiseGreedyAdjacencyMatrixWithCheapestPath(vertices2, adjacencyMatrix2, cheapestPath, vertices1, greedyVertices, greedyAdjMatrix)

        # Write the greedy adjacency matrix and vertices to a file with the appropriate formatting
        writeMatrixToFile(graphOutputFileName, greedyVertices, greedyAdjMatrix)

        # Write whether the greedy graph is connected or not to the output file
        writeConnectivityToFile(greedyVertices, greedyAdjMatrix, graphOutputFileName)
    else:
        print("A valid intermediate graph is required to solve this problem.")

def main():
    # Prompt the user for input graph files
    graphInputFileName1 = input("Enter input file name: ")
    graphInputFileName2 = input("Enter input file name: ")
    graphInputFileName3 = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph files
    vertices1 = getVerticesFromFile(graphInputFileName1)
    adjacencyMatrix1 = getAdjacencyMatrixFromFile(graphInputFileName1)
    intermediateVertices = getVerticesFromFile(graphInputFileName2)
    intermediateAdjacencyMatrix = getAdjacencyMatrixFromFile(graphInputFileName2)
    vertices3 = getVerticesFromFile(graphInputFileName3)
    adjacencyMatrix3 = getAdjacencyMatrixFromFile(graphInputFileName3)

    # Write the greedy adjacency matrix and vertices to the output graph file with the appropriate formatting
    writeGreedyAdjacencyMatrixToFile(vertices1, intermediateVertices, vertices3, adjacencyMatrix1, intermediateAdjacencyMatrix, adjacencyMatrix3, graphInputFileName1, graphInputFileName2, graphInputFileName3)

if __name__ == "__main__":
    main()