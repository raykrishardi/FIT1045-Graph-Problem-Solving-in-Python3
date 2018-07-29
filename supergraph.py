# ----------------------------------------------------------------------------------------------------------------------
#                                             Name: Ray Krishardi Layadi
#                                              Student ID: 26445549
# ----------------------------------------------------------------------------------------------------------------------

# Import the required functions from the graphFileOps.py, intersection.py, and union.py file
from graphFileOps import getVerticesFromFile, getAdjacencyMatrixFromFile, writeMatrixToFile
from intersection import getIntersectVertices, checkAndGetIntersectVertices, getIntersectEdges, getValidIntersectEdges, getAdjacencyMatrix
from union import getUnionVertices, initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection, initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight

# Function that returns the supergraph's valid intersect edges
# This function basically reduces the amount of code to be written by just returning the valid intersect edges (i.e. the
# creation of the intersect vertices and edges are handled in this function)
def getSupergraphValidIntersectEdges(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2):
    # Get the intersect vertices, intersect edges, and valid intersect edges
    intersectVertices = checkAndGetIntersectVertices(vertices1, vertices2)
    intersectEdges = getIntersectEdges(intersectVertices, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
    validIntersectEdges = getValidIntersectEdges(intersectEdges)

    return validIntersectEdges

# Function that swaps graphs given two index of the element to be swapped in the graphs list
def swapGraphs(graphs, x, y):
    tmp = graphs[x]
    graphs[x] = graphs[y]
    graphs[y] = tmp

# Function that checks when to perform graph swapping to make sure that the intermediate graph occupies the middle section
# In addition, this function will also return the appropriate flag to indicate whether an intermediate graph exist or not
# in the given 3 graph input files
def checkSwapGraphsAndGetIntermediateGraphExistFlag(graphs):
    intermediateGraphExist = True

    # Check for intermediate graph and swap its position to the middle section if it is not in the middle part
    # This is done by calculating the length of the intersect vertices
    # (e.g. since H is the intermediate graph between graphs G and I, the result of the intersection between G and H
    # and I and H will at least result in 1 intersect vertices. On the other hand, the result of the intersection between
    # graphs G and I will result in 0 intersect vertices)
    if len(getIntersectVertices(graphs[0][0], graphs[1][0])) != 0 and len(getIntersectVertices(graphs[1][0], graphs[2][0])) != 0:
        pass  # Perform nothing if the intermediate graph is already in the middle section
    elif len(getIntersectVertices(graphs[0][0], graphs[1][0])) == 0 and len(getIntersectVertices(graphs[1][0], graphs[2][0])) != 0:
        swapGraphs(graphs, 1, 2)  # Swap the intermediate graph to the middle section
    elif len(getIntersectVertices(graphs[0][0], graphs[1][0])) != 0 and len(getIntersectVertices(graphs[1][0], graphs[2][0])) == 0:
        swapGraphs(graphs, 0, 1)  # Swap the intermediate graph to the middle section
    else:
        intermediateGraphExist = False  # Assign False to the flag if all of the criteria is not met

    return intermediateGraphExist

# Function that writes the supergraph adjacency matrix and vertices to a file with the appropriate formatting
def writeSupergraphAdjacencyMatrixToFile(vertices1, vertices2, vertices3, adjacencyMatrix1, adjacencyMatrix2, adjacencyMatrix3, fileName1, fileName2, fileName3):
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
    graphOutputFileName = "supergraph" + fileName1[:len(fileName1)-4] + fileName2[:len(fileName2)-4] + fileName3[:len(fileName3)-4] + ".txt"

    # Get the supergraph vertices and adjacency matrix which contains all vertices in vertices 1, 2, and 3
    supergraphVertices = getUnionVertices(vertices1, vertices2)
    supergraphVertices = getUnionVertices(supergraphVertices, vertices3)
    supergraphAdjMatrix = getAdjacencyMatrix(supergraphVertices)

    # Check whether an intermediate graph exist or not
    if intermediateGraphExist:
        # Get the intersect edges between vertices 1 and 2 and vertices 3 and 2
        validIntersectEdges1 = getSupergraphValidIntersectEdges(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
        validIntersectEdges2 = getSupergraphValidIntersectEdges(vertices3, vertices2, adjacencyMatrix3, adjacencyMatrix2)

        # Initialise the supergraph adjacency matrix with adjacency matrix 1, 2, 3's weights while excluding weights from
        # intersect edges (intersect of vertices 1 and 2 and vertices 3 and 2)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices1, adjacencyMatrix1, validIntersectEdges1, validIntersectEdges2, [], supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices2, adjacencyMatrix2, validIntersectEdges1, validIntersectEdges2, [], supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices3, adjacencyMatrix3, validIntersectEdges1, validIntersectEdges2, [], supergraphVertices, supergraphAdjMatrix)

        # Initialise the supergraph adjacency matrix with smallest weight from adjacency matrix 1 or 2 and
        # adjacency matrix 3 or 2 by using the intersect edges (intersect of vertices 1 and 2 and vertices 3 and 2)
        # This is achieved by comparing the weight in adjacency matrix 1, 2, and 3 that correlates with the intersect edges
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges1, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges2, vertices3, vertices2, adjacencyMatrix3, adjacencyMatrix2, supergraphVertices, supergraphAdjMatrix)
    else:
        # If intermediate graph does NOT exist, we need to check whether each graph has intersect edges with one another
        # In this case, get the intersect edges between vertices 1 and 2, vertices 3 and 2, and vertices 1 and 3
        validIntersectEdges1 = getSupergraphValidIntersectEdges(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
        validIntersectEdges2 = getSupergraphValidIntersectEdges(vertices1, vertices3, adjacencyMatrix1, adjacencyMatrix3)
        validIntersectEdges3 = getSupergraphValidIntersectEdges(vertices2, vertices3, adjacencyMatrix2, adjacencyMatrix3)

        # Initialise the supergraph adjacency matrix with adjacency matrix 1, 2, 3's weights while excluding weights from
        # intersect edges (intersect of vertices 1 and 2, vertices 3 and 2, and vertices 1 and 3)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices1, adjacencyMatrix1, validIntersectEdges1,
                                                          validIntersectEdges2, validIntersectEdges3, supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices2, adjacencyMatrix2, validIntersectEdges1,
                                                          validIntersectEdges2, validIntersectEdges3, supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices3, adjacencyMatrix3, validIntersectEdges1,
                                                          validIntersectEdges2, validIntersectEdges3, supergraphVertices, supergraphAdjMatrix)

        # Initialise the supergraph adjacency matrix with smallest weight from adjacency matrix 1 or 2 and
        # adjacency matrix 3 or 2 and adjacency matrix 1 or 3 by using the intersect edges (intersect of
        # vertices 1 and 2, vertices 3 and 2, and vertices 1 and 3)
        # This is achieved by comparing the weight in adjacency matrix 1, 2, and 3 that correlates with the intersect edges
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges1, vertices1, vertices2, adjacencyMatrix1,
                                                         adjacencyMatrix2, supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges2, vertices1, vertices3, adjacencyMatrix1,
                                                         adjacencyMatrix3, supergraphVertices, supergraphAdjMatrix)
        initTargetAdjMatrixWithIntersectEdgesWithSmallestWeight(validIntersectEdges3, vertices2, vertices3, adjacencyMatrix2,
                                                         adjacencyMatrix3, supergraphVertices, supergraphAdjMatrix)

    # Write the supergraph adjacency matrix and vertices to a file with the appropriate formatting
    writeMatrixToFile(graphOutputFileName, supergraphVertices, supergraphAdjMatrix)

def main():
    # Prompt the user for input graph files
    graphInputFileName1 = input("Enter input file name: ")
    graphInputFileName2 = input("Enter input file name: ")
    graphInputFileName3 = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph files
    vertices1 = getVerticesFromFile(graphInputFileName1)
    adjacencyMatrix1 = getAdjacencyMatrixFromFile(graphInputFileName1)
    vertices2 = getVerticesFromFile(graphInputFileName2)
    adjacencyMatrix2 = getAdjacencyMatrixFromFile(graphInputFileName2)
    vertices3 = getVerticesFromFile(graphInputFileName3)
    adjacencyMatrix3 = getAdjacencyMatrixFromFile(graphInputFileName3)

    # Write the supergraph adjacency matrix and vertices to the output graph file with the appropriate formatting
    writeSupergraphAdjacencyMatrixToFile(vertices1, vertices2, vertices3, adjacencyMatrix1, adjacencyMatrix2, adjacencyMatrix3, graphInputFileName1, graphInputFileName2, graphInputFileName3)

if __name__ == "__main__":
    main()