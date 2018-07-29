# ----------------------------------------------------------------------------------------------------------------------
#                                             Name: Ray Krishardi Layadi
#                                              Student ID: 26445549
# ----------------------------------------------------------------------------------------------------------------------

# Import the required functions from the graphFileOps.py, intersection.py, and union.py file
from graphFileOps import getVerticesFromFile, getAdjacencyMatrixFromFile, writeMatrixToFile, getIndex, popElementAtIndex
from intersection import checkAndGetIntersectVertices, getIntersectEdges, getValidIntersectEdges, getAdjacencyMatrix
from union import getUnionVertices, initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection

# Function that returns invalid vertices
# In this case, invalid vertices are vertices that have no edges (i.e. total weight of each invalid vertex's row is 0)
# For example, in finding the difference of graph G and H, vertex 'c' has no edges as difference does not include the intersect edges
# Therefore, vertex 'c' is considered as invalid and will need to be removed from the difference vertices and adjacency matrix
def getInvalidVertices(differenceVertices, differenceAdjMatrix):
    invalidVertices = []

    # Loop through each vertex in the difference adjacency matrix
    for row in range(len(differenceAdjMatrix)):
        totalWeight = 0

        # Calculate the total weight of the selected vertex
        for col in range(len(differenceAdjMatrix[row])):
            totalWeight += differenceAdjMatrix[row][col]

        # If the total weight of the selected vertex is 0 (vertex has no edges) then add the vertex to the list of invalid vertices
        if totalWeight == 0:
            invalidVertices.append(differenceVertices[row])

    return invalidVertices

# Function that removes the invalid vertices from the difference vertices and adjacency matrix
def removeInvalidVerticesFromDifferenceAdjacencyMatrix(differenceVertices, differenceAdjMatrix, invalidVertices):
    # Loop through each invalid vertices
    for invalidVertex in invalidVertices:
        # Get the index of the invalid vertex in difference vertices
        invalidVertexIndex = getIndex(differenceVertices, invalidVertex)

        # Remove the invalid vertex's weight from the difference adjacency matrix
        for row in range(len(differenceAdjMatrix)):
            differenceAdjMatrix[row].pop(invalidVertexIndex)

        # Remove the invalid vertex from the difference vertices and adjacency matrix
        differenceVertices.pop(invalidVertexIndex)
        differenceAdjMatrix.pop(invalidVertexIndex)

# Function that writes the difference adjacency matrix and vertices to a file with the appropriate formatting
def writeDifferenceAdjacencyMatrixToFile(vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2, fileName1, fileName2):
    # Generate the output file name
    # This is done by removing the ".txt" extension from the file names and concatenate the required additional string
    # at the middle of it and adding a new .txt extension at the end of it
    graphOutputFileName = fileName1[:len(fileName1)-4] + "_xor_" + fileName2[:len(fileName2)-4] + ".txt"

    # Get the intersect vertices, intersect edges, and valid intersect edges
    intersectVertices = checkAndGetIntersectVertices(vertices1, vertices2)
    intersectEdges = getIntersectEdges(intersectVertices, vertices1, vertices2, adjacencyMatrix1, adjacencyMatrix2)
    validIntersectEdges = getValidIntersectEdges(intersectEdges)

    # Get the difference vertices and adjacency matrix
    # Initially, differenceVertices = unionVertices and differenceAdjMatrix = unionAdjMatrix
    # Because initially, just like the union vertices and adjacency matrix, the difference vertices and adjacency matrix includes all vertices
    differenceVertices = getUnionVertices(vertices1, vertices2)
    differenceAdjMatrix = getAdjacencyMatrix(differenceVertices)

    # Initialise the difference adjacency matrix with adjacency matrix 1's weights while excluding weights from intersect edges (intersect of vertices 1 and 2)
    initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices1, adjacencyMatrix1, validIntersectEdges, [], [],
                                                              differenceVertices, differenceAdjMatrix)

    # Initialise the difference adjacency matrix with adjacency matrix 2's weights while excluding weights from intersect edges (intersect of vertices 1 and 2)
    initTargetAdjMatrixWithSourceAdjMatrixWithoutIntersection(vertices2, adjacencyMatrix2, validIntersectEdges, [], [],
                                                              differenceVertices, differenceAdjMatrix)

    # Get the invalid vertices and remove the invalid vertices from the difference vertices and adjacency matrix
    invalidVertices = getInvalidVertices(differenceVertices, differenceAdjMatrix)
    removeInvalidVerticesFromDifferenceAdjacencyMatrix(differenceVertices, differenceAdjMatrix, invalidVertices)

    # Write the difference adjacency matrix and vertices to a file with the appropriate formatting
    writeMatrixToFile(graphOutputFileName, differenceVertices, differenceAdjMatrix)

def main():
    # Prompt the user for input graph files
    graphInputFileName1 = input("Enter input file name: ")
    graphInputFileName2 = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph files
    vertices1 = getVerticesFromFile(graphInputFileName1)
    adjacencyMatrix = getAdjacencyMatrixFromFile(graphInputFileName1)
    vertices2 = getVerticesFromFile(graphInputFileName2)
    adjacencyMatrix2 = getAdjacencyMatrixFromFile(graphInputFileName2)

    # Write the difference adjacency matrix and vertices to the output graph file with the appropriate formatting
    writeDifferenceAdjacencyMatrixToFile(vertices1, vertices2, adjacencyMatrix, adjacencyMatrix2, graphInputFileName1, graphInputFileName2)

if __name__ == "__main__":
    main()