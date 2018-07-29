# ----------------------------------------------------------------------------------------------------------------------
#                                             Name: Ray Krishardi Layadi
#                                              Student ID: 26445549
# ----------------------------------------------------------------------------------------------------------------------

# Import the required functions from the graphFileOps.py and intersection.py file
from graphFileOps import getVerticesFromFile, getAdjacencyMatrixFromFile, writeMatrixToFile, getIndex
from intersection import checkAndGetIntersectVertices, getIntersectEdges, getValidIntersectEdges, getAdjacencyMatrix

# Function that returns the union vertices given two vertices
def getUnionVertices(vertices1, vertices2):
    unionVertices = vertices1 + vertices2  # Union vertices that contains duplicate vertices (e.g. 'a' and 'a')
    validUnionVertices = []  # Union vertices that does NOT contain duplicate vertices (i.e. each vertex is unique)

    # Loop through each vertex in union vertices that contains duplicate vertices
    for vertex in unionVertices:
        # If the vertex is not in union vertices that does NOT contain duplicate vertices then add that vertex to the
        # valid union vertices list
        if vertex not in validUnionVertices:
            validUnionVertices.append(vertex)

    return validUnionVertices  # Return the union vertices that does NOT contain duplicate vertices

# Function that checks whether a given edge is in the valid intersect edges
def edgeInValidIntersectEdges(edge, validIntersectEdges):
    # Loop through each valid intersect edges
    for validIntersectEdge in validIntersectEdges:
        # If the given edge is in the valid intersect edges then return True
        if edge[0] in validIntersectEdge and edge[1] in validIntersectEdge:
            return True
    return False  # If the given edge is NOT in the valid intersect edges then return False

# Function that initialises the target adjacency matrix with the source adjacency matrix's weights
# while excluding any intersection edges
def initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(sourceVertices, sourceAdjMatrix, validIntersectEdges1, validIntersectEdges2, validIntersectEdges3, targetVertices, targetAdjMatrix):
    # Loop through each vertex in the source vertices
    for i in range(len(sourceVertices)):
        # Find the index of the source vertex in source and target vertices
        # This is because the index of the source vertex differ from source and target vertices
        vertex1IndexInSourceVertices = getIndex(sourceVertices, sourceVertices[i])
        vertex1IndexInTargetVertices = getIndex(targetVertices, sourceVertices[i])

        # Loop through each vertex in the source vertices again because we want to get the edges
        for j in range(len(sourceVertices)):
            # Find the index of the source vertex in source and target vertices
            # This is because the index of the source vertex differ from source and target vertices
            vertex2IndexInSourceVertices = getIndex(sourceVertices, sourceVertices[j])
            vertex2IndexInTargetVertices = getIndex(targetVertices, sourceVertices[j])

            # Create edge from source vertices
            edge = [sourceVertices[vertex1IndexInSourceVertices], sourceVertices[vertex2IndexInSourceVertices]]

            # Only process different source vertices (exclude same vertices (e.g. index of 'a' and 'a'))
            if vertex1IndexInSourceVertices != vertex2IndexInSourceVertices:
                # Check the value of the weight in source adjacency matrix (there is an edge if the weight is not equal to 0)
                # In addition, only assign the weight to the target adjacency matrix if the edge is NOT in any of the intersect edges
                if sourceAdjMatrix[vertex1IndexInSourceVertices][vertex2IndexInSourceVertices] != 0 and \
                        not edgeInValidIntersectEdges(edge, validIntersectEdges1) and \
                        not edgeInValidIntersectEdges(edge, validIntersectEdges2) and \
                        not edgeInValidIntersectEdges(edge, validIntersectEdges3):
                    targetAdjMatrix[vertex1IndexInTargetVertices][vertex2IndexInTargetVertices] = sourceAdjMatrix[vertex1IndexInSourceVertices][vertex2IndexInSourceVertices]

# Function that initialises the target adjacency matrix with the smallest weight from adjacency matrix 1 or 2 given an intersect edges
# This is achieved by comparing the weight in adjacency matrix 1 and 2
def initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(intersectEdges, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, targetVertices, targetAdjMatrix):
    # Loop through each edge in the intersect edges
    for edge in intersectEdges:
        # Get the index of the intersect vertices in vertices 1 and 2
        vertex1IndexInVertices1 = getIndex(vertices1, edge[0])
        vertex1IndexInVertices2 = getIndex(vertices2, edge[0])
        vertex2IndexInVertices1 = getIndex(vertices1, edge[1])
        vertex2IndexInVertices2 = getIndex(vertices2, edge[1])

        # Get the index of the intersect vertices in target vertices
        vertex1IndexInTargetVertices = getIndex(targetVertices, edge[0])
        vertex2IndexInTargetVertices = getIndex(targetVertices, edge[1])

        # Compare the weight of the intersect vertices in adjacency matrix 1 and 2
        # Assign weight to the smaller weight
        if adjacencyMatrix1[vertex1IndexInVertices1][vertex2IndexInVertices1] <= adjacencyMatrix2[vertex1IndexInVertices2][vertex2IndexInVertices2]:
            weight = adjacencyMatrix1[vertex1IndexInVertices1][vertex2IndexInVertices1]
        else:
            weight = adjacencyMatrix2[vertex1IndexInVertices2][vertex2IndexInVertices2]

        # Assign smaller weight to the target adjacency matrix
        targetAdjMatrix[vertex1IndexInTargetVertices][vertex2IndexInTargetVertices] = weight
        targetAdjMatrix[vertex2IndexInTargetVertices][vertex1IndexInTargetVertices] = weight

# Function that writes the union adjacency matrix and vertices to a file with the appropriate formatting
def writeUnionAdjacencyMatrixToFile(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, fileName1, fileName2):
    # Generate the output file name
    # This is done by removing the ".txt" extension from the file names and concatenate the required additional string
    # at the middle of it and adding a new .txt extension at the end of it
    graphOutputFileName = fileName1[:len(fileName1)-4] + "_or_" + fileName2[:len(fileName2)-4] + ".txt"

    # Get the intersect vertices, intersect edges, and valid intersect edges
    intersectVertices = checkAndGetIntersectVertices(vertices1, vertices2)
    intersectEdges = getIntersectEdges(intersectVertices, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
    validIntersectEdges = getValidIntersectEdges(intersectEdges)

    # Get the union vertices and adjacency matrix
    unionVertices = getUnionVertices(vertices1, vertices2)
    unionAdjMatrix = getAdjacencyMatrix(unionVertices)

    # Initialise the union adjacency matrix with adjacency matrix 1's weights while excluding weights from intersect edges (intersect of vertices 1 and 2)
    initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices1, adjacencyMatrix1, validIntersectEdges, [], [], unionVertices, unionAdjMatrix)

    # Initialise the union adjacency matrix with adjacency matrix 2's weights while excluding weights from intersect edges (intersect of vertices 1 and 2)
    initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices2, adjacencyMatrix2, validIntersectEdges, [], [], unionVertices, unionAdjMatrix)

    # Initialise the union adjacency matrix with smallest weight from adjacency matrix 1 or 2 by using the intersect edges (intersect of vertices 1 and 2)
    # This is achieved by comparing the weight in adjacency matrix 1 and 2 that correlates with the intersect edges
    initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, unionVertices, unionAdjMatrix)

    # Write the union adjacency matrix and vertices to a file with the appropriate formatting
    writeMatrixToFile(graphOutputFileName, unionVertices, unionAdjMatrix)

def main():
    # Prompt the user for input graph files
    graphInputFileName1 = input("Enter input file name: ")
    graphInputFileName2 = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph files
    vertices1 = getVerticesFromFile(graphInputFileName1)
    adjacencyMatrix = getAdjacencyMatrixFromFile(graphInputFileName1)
    vertices2 = getVerticesFromFile(graphInputFileName2)
    adjacencyMatrix2 = getAdjacencyMatrixFromFile(graphInputFileName2)

    # Write the union adjacency matrix and vertices to the output graph file with the appropriate formatting
    writeUnionAdjacencyMatrixToFile(vertices1, vertices2, adjacencyMatrix, adjacencyMatrix2, graphInputFileName1, graphInputFileName2)

if __name__ == "__main__":
    main()