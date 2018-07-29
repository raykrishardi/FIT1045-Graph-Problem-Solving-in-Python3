# ----------------------------------------------------------------------------------------------------------------------
#                                             Name: Ray Krishardi Layadi
#                                              Student ID: 26445549
# ----------------------------------------------------------------------------------------------------------------------

# Import the required functions from the graphFileOps.py file
from graphFileOps import getVerticesFromFile, getAdjacencyMatrixFromFile, popElementAtIndex, getElementAtIndex

# Function that writes a single line to a file
def writeLineToFile(fileName, line):
    graphOutputFile = open(fileName, 'w')  # Open the file for writing
    graphOutputFile.write(line)  # Write line to file
    graphOutputFile.close()  # Close the file

# Function that writes whether the given supergraph (or any combined graph) file is connected or not to the output file
def writeConnectivityToFile(vertices, adjacencyMatrix, fileName):
    # Generate the output file name
    # This is done by removing the ".txt" extension from the file name and concatenate the required additional string
    # at the end of it
    outputFileName = fileName[:len(fileName)-4] + "connectivity.txt"

    # Line to be written to the output file (Initially, "graph IS connected")
    line = "graph IS connected"

    # Queue of vertices to be processed/served
    verticesQueue = []

    # List that represents whether a particular vertex has been visited or not
    visited = [False]*len(vertices)

    # Append the first vertex (denoted by index 0) in the list of vertices to the queue
    # In addition, indicate that the first vertex has been visited as the vertex is already in the queue to be processed
    verticesQueue.append(0)
    visited[0] = True

    # Loop through each vertices in the queue
    while len(verticesQueue) > 0:
        vertexIndex = getElementAtIndex(verticesQueue, 0) # Get the index of the vertex to be processed
        verticesQueue = popElementAtIndex(verticesQueue, 0)  # Pop the queue at index 0

        # Loop through each vertices
        for i in range(len(vertices)):
            # If the vertex to be processed has an edge (there must be at least 1 non-zero weight in that vertex's row)
            # then append the adjacent vertex to the queue to be processed and indicate that the adjacent vertex has been visited
            if adjacencyMatrix[vertexIndex][i] != 0 and (not visited[i]):
                verticesQueue.append(i)
                visited[i] = True

    # If there is at least 1 vertex that has NOT been visited then indicate that the "graph is NOT connected"
    if False in visited:
        line = "graph IS NOT connected"

    # Write whether the supergraph (or any combined graph) is connected or not to the output file
    writeLineToFile(outputFileName, line)

def main():
    # Prompt the user for input graph file
    # In this case, it is a supergraph (or any combined graph) file
    graphInputFileName1 = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph file
    vertices1 = getVerticesFromFile(graphInputFileName1)
    adjacencyMatrix1 = getAdjacencyMatrixFromFile(graphInputFileName1)

    # Function that writes whether the given supergraph (or any combined graph) file is connected or not to the output file
    writeConnectivityToFile(vertices1, adjacencyMatrix1, graphInputFileName1)

if __name__ == "__main__":
    main()