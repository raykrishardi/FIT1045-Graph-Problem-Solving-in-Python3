# ----------------------------------------------------------------------------------------------------------------------
#                                             Name: Ray Krishardi Layadi
#                                              Student ID: 26445549
# ----------------------------------------------------------------------------------------------------------------------

# Import the required functions from the graphFileOps.py file
from graphFileOps import getVerticesFromFile, getAdjacencyMatrixFromFile, writeMatrixToFile, getIndex

# Function that returns the intersect vertices given two vertices
def getIntersectVertices(vertices1, vertices2):
    intersectVertices = []

    # Loop through each vertex in vertices 1 and 2
    # If they are equal then append the vertex to the list of intersect vertices
    for vertex1 in vertices1:
        for vertex2 in vertices2:
            if vertex1 == vertex2:
                intersectVertices.append(vertex1)

    return intersectVertices

# Function that checks and gets the appropriate intersect vertices given two vertices
def checkAndGetIntersectVertices(vertices1, vertices2):
    # Check the number of vertices in vertices 1 and 2 and get the appropriate intersect vertices
    # We need to check the number of vertices because we want to loop through the larger vertices in the outer loop
    # so that we can cover every vertex in the larger vertices and compare it with the smaller one
    if len(vertices1) > len(vertices2):
        return getIntersectVertices(vertices1, vertices2)
    else:
        return getIntersectVertices(vertices2, vertices1)

# Function that returns the intersect edges given the intersect vertices
# In this case, the intersect edges contains duplicate edges (e.g. ['a', 'c'] and ['c', 'a'])
def getIntersectEdges(intersectVertices, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2):
    intersectEdges = []

    # Loop through each vertex in the intersect vertices
    for i in range(len(intersectVertices)):
        # Find the index of the intersect vertex in vertices 1 and 2
        # This is because the index of the intersect vertex differ from vertices 1 and 2
        vertex1IndexInVertices1 = getIndex(vertices1, intersectVertices[i])
        vertex1IndexInVertices2 = getIndex(vertices2, intersectVertices[i])

        # Loop through each vertex in the intersect vertices again because we want to get the intersect edges
        for j in range(len(intersectVertices)):
            # Find the index of the intersect vertex in vertices 1 and 2
            # This is because the index of the intersect vertex differ from vertices 1 and 2
            vertex2IndexInVertices1 = getIndex(vertices1, intersectVertices[j])
            vertex2IndexInVertices2 = getIndex(vertices2, intersectVertices[j])

            # Only process different intersect vertices (exclude same vertices (e.g. index of 'a' and 'a'))
            if vertex1IndexInVertices1 != vertex2IndexInVertices1 and vertex1IndexInVertices2 != vertex2IndexInVertices2:
                # Get the intersect edges by checking the value of the weight in adjacencyMatrix 1 and 2 (there is an edge if the weight is not equal to 0)
                if adjacencyMatrix1[vertex1IndexInVertices1][vertex2IndexInVertices1] != 0 and adjacencyMatrix2[vertex1IndexInVertices2][vertex2IndexInVertices2] != 0:
                    intersectEdges.append([intersectVertices[i], intersectVertices[j]])

    return intersectEdges

# Function that returns a valid intersect edges given an intersect edges
# In this case, the valid intersect edges does NOT contain duplicate edges (e.g. ['a', 'c'] and ['c', 'a'])
def getValidIntersectEdges(intersectEdges):
    validIntersectEdges = []

    # Loop through each edge in the intersect edges
    for i in range(len(intersectEdges)):
        # Get the vertices from the intersect edges
        vertex1 = intersectEdges[i][0]
        vertex2 = intersectEdges[i][1]

        # Loop through each edge in the intersect edges again because we want to eliminate duplicate edges
        for j in range(i+1, len(intersectEdges)):
            # If there is an edge that is a duplicate (e.g. ['a', 'c'] and ['c', 'a']) then add one of the edge to the
            # list of valid intersect edges
            if vertex1 in intersectEdges[j] and vertex2 in intersectEdges[j]:
                validIntersectEdges.append(intersectEdges[i])

    return validIntersectEdges

# Function that returns a valid intersect vertices by using the valid intersect edges
# In this case, the valid intersect vertices does NOT contain vertices that are NOT actually used in the intersection
# For example, in finding the intersection of graph G and H, vertex 'Q' is not actually used in the intersection (i.e. no edges connecting 'Q')
# Therefore, vertex 'Q' is not included in the valid intersect vertices
def getValidIntersectVertices(validIntersectEdges):
    validIntersectVertices = []

    # Loop through each edge in the valid intersect edges
    for validEdge in validIntersectEdges:
        # Get vertices from edge
        vertex1 = validEdge[0]
        vertex2 = validEdge[1]

        # Check whether each vertex in the edge is already included in the valid intersect vertices
        # If not then add that vertex to the valid intersect vertices
        if vertex1 not in validIntersectVertices:
            validIntersectVertices.append(vertex1)
        if vertex2 not in validIntersectVertices:
            validIntersectVertices.append(vertex2)

    return validIntersectVertices

# Function that returns the appropriate adjacency matrix based on the given vertices
# In this case, the function will return the intersect adjacency matrix
def getAdjacencyMatrix(vertices):
    adjMatrix = []

    # Initialise the adjacency matrix based on the number of vertices
    for _ in range(len(vertices)):
        adjMatrix.append([0] * len(vertices))

    return adjMatrix

# Function that initialises the intersect adjacency matrix with the largest weight from adjacency matrix 1 or 2
# This is achieved by comparing the weight in adjacency matrix 1 and 2
def initialiseIntersectAdjacencyMatrixWithLargestWeight(intersectAdjMatrix, validIntersectVertices, validIntersectEdges, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2):
    # Loop through each edge in the valid intersect edges
    for edge in validIntersectEdges:
        # Get the index of the intersect vertices in vertices 1 and 2
        vertex1IndexInVertices1 = getIndex(vertices1, edge[0])
        vertex1IndexInVertices2 = getIndex(vertices2, edge[0])
        vertex2IndexInVertices1 = getIndex(vertices1, edge[1])
        vertex2IndexInVertices2 = getIndex(vertices2, edge[1])

        # Get the index of the intersect vertices in valid intersect vertices
        vertex1IndexInIntersectVertices = getIndex(validIntersectVertices, edge[0])
        vertex2IndexInIntersectVertices = getIndex(validIntersectVertices, edge[1])

        # Compare the weight of the intersect vertices in adjacency matrix 1 and 2
        # Assign weight to the larger weight
        if adjacencyMatrix1[vertex1IndexInVertices1][vertex2IndexInVertices1] >= adjacencyMatrix2[vertex1IndexInVertices2][vertex2IndexInVertices2]:
            weight = adjacencyMatrix1[vertex1IndexInVertices1][vertex2IndexInVertices1]
        else:
            weight = adjacencyMatrix2[vertex1IndexInVertices2][vertex2IndexInVertices2]

        # Assign larger weight to the intersect adjacency matrix
        intersectAdjMatrix[vertex1IndexInIntersectVertices][vertex2IndexInIntersectVertices] = weight
        intersectAdjMatrix[vertex2IndexInIntersectVertices][vertex1IndexInIntersectVertices] = weight

# Function that writes the intersect adjacency matrix and vertices to a file with the appropriate formatting
def writeIntersectAdjacencyMatrixToFile(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, fileName1, fileName2):
    # Generate the output file name
    # This is done by removing the ".txt" extension from the file names and concatenate the required additional string
    # at the middle of it and adding a new .txt extension at the end of it
    graphOutputFileName = fileName1[:len(fileName1)-4] + "_and_" + fileName2[:len(fileName2)-4] + ".txt"

    # Get the intersect vertices and edges, valid intersect vertices and edges, and intersect adjacency matrix
    intersectVertices = checkAndGetIntersectVertices(vertices1, vertices2)
    intersectEdges = getIntersectEdges(intersectVertices, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
    validIntersectEdges = getValidIntersectEdges(intersectEdges)
    validIntersectVertices = getValidIntersectVertices(validIntersectEdges)
    intersectAdjMatrix = getAdjacencyMatrix(validIntersectVertices)

    # Initialise the intersect adjacency matrix with largest weight from adjacency matrix 1 or 2
    # This is achieved by comparing the weight in adjacency matrix 1 and 2
    initialiseIntersectAdjacencyMatrixWithLargestWeight(intersectAdjMatrix, validIntersectVertices, validIntersectEdges, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)

    # Write the intersect adjacency matrix and vertices to a file with the appropriate formatting
    writeMatrixToFile(graphOutputFileName, validIntersectVertices, intersectAdjMatrix)

def main():
    # Prompt the user for input graph files
    graphInputFileName1 = input("Enter input file name: ")
    graphInputFileName2 = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph files
    vertices1 = getVerticesFromFile(graphInputFileName1)
    adjacencyMatrix1 = getAdjacencyMatrixFromFile(graphInputFileName1)
    vertices2 = getVerticesFromFile(graphInputFileName2)
    adjacencyMatrix2 = getAdjacencyMatrixFromFile(graphInputFileName2)

    # Write the intersect adjacency matrix and vertices to the output graph file with the appropriate formatting
    writeIntersectAdjacencyMatrixToFile(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, graphInputFileName1, graphInputFileName2)

if __name__ == "__main__":
    main()