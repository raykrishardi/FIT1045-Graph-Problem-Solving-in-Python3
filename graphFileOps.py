# ----------------------------------------------------------------------------------------------------------------------
#                                             Name: Ray Krishardi Layadi
#                                              Student ID: 26445549
# ----------------------------------------------------------------------------------------------------------------------

# Function that returns a list of vertices from the given graph file
def getVerticesFromFile(fileName):
    graphInputFile = open(fileName, 'r')  # Open the graph file for reading

    # Get the list of vertices from the graph file by reading the first line of the graph file
    # and use the ':' character as the delimiter
    vertices = graphInputFile.readline().strip('\n').split(':')

    graphInputFile.close()  # Close the graph file
    return vertices  # Return the list of vertices from the graph file

# Function that returns an adjacency matrix from the given graph file
def getAdjacencyMatrixFromFile(fileName):
    graphInputFile = open(fileName, 'r')  # Open the graph file for reading

    # Create an adjacency matrix from the graph file by iterating through the graph file starting from the second line
    adjMatrix = []
    for lineNumber, line in enumerate(graphInputFile):
        if lineNumber != 0:
            adjMatrix.append([int(i) for i in line.split()])

    graphInputFile.close()  # Close the graph file
    return adjMatrix  # Return the adjacency matrix from the graph file

# Function that prints the list of vertices in a well suited format (each vertex is separated by a tab)
# for debugging purposes
def printVertices(vertices):
    line = ""
    for vertex in vertices:
        line += vertex + '\t'
    print(line)

# Function that prints the adjacency matrix in a well suited format (each weight is separated by a tab)
# for debugging purposes
def printMatrix(matrix):
    for row in range(len(matrix)):
        line = ""
        for col in range(len(matrix[row])):
            line += str(matrix[row][col]) + '\t'
        line += '\n'
        print(line)

# Function that writes the adjacency matrix and vertices to a file with the appropriate formatting
# Format:
# 1. Each vertex is separated by a ':'
# 2. Each weight in the adjacency matrix is separated by a ' '
def writeMatrixToFile(fileName, vertices, matrix):
    graphOutputFile = open(fileName, 'w')  # Open the graph file for writing
    verticesLine = "" # Represent the vertices separated by a ':' to be written to the graph file

    # Loop through each vertex and concatenate the vertex with ':'
    for i in range(len(vertices)):
        verticesLine += vertices[i] + ':'

    # Remove the last ':' character from the string and add a newline character
    verticesLine = verticesLine[:-1] + '\n'

    # Write the vertices to the graph file with the appropriate formatting
    graphOutputFile.write(verticesLine)

    # Write the adjacency matrix to the graph file with the appropriate formatting
    for row in range(len(matrix)):
        line = ""
        for weight in matrix[row]:
            line += str(weight) + " "
        # Exclude new line for the last row in the adjacency matrix
        if row != len(matrix)-1:
            line += '\n'
        graphOutputFile.write(line)

    graphOutputFile.close()  # Close the graph file

# ----------------------------------------------------------------------------------------------------------------------
#                                             Additional Functions
# ----------------------------------------------------------------------------------------------------------------------

# List built-in "index" function
def getIndex(aList, target):
    for i in range(len(aList)):
        if aList[i] == target:
            return i
    return -1

# "in" built-in function
def inLinearSearch(aList, target):
    for i in range(len(aList)):
        if aList[i] == target:
            return True
    return False

# List built-in "pop" function
def popLastElement(aList):
    return aList[:-1]

# List built-in "pop" at index function (in this case, it returns a list instead of the popped element)
def popElementAtIndex(aList, index):
    return aList[:index] + aList[index+1:]

# Function that returns the element of the list specified by the index
def getElementAtIndex(aList, index):
    return aList[index]

# ----------------------------------------------------------------------------------------------------------------------

def main():
    # Prompt the user for an input graph file
    graphInputFileName = input("Enter input file name: ")

    # Get the vertices and adjacency matrix from the graph file
    vertices = getVerticesFromFile(graphInputFileName)
    adjacencyMatrix = getAdjacencyMatrixFromFile(graphInputFileName)

    # Prompt the user for the file name of the output graph file
    graphOutputFileName = input("Enter output file name: ")

    # Write the adjacency matrix and vertices to the output graph file with the appropriate formatting
    writeMatrixToFile(graphOutputFileName, vertices, adjacencyMatrix)

if __name__ == "__main__":
    main()