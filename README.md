# Graph Problem Solving in Python3

# About the project:
This project is my first assignment for the FIT1045 (Algorithms and Programming Fundamentals in Python) unit. The project involves solving several graph related problems. Below contains the descriptions of the problems which are directly taken from the assignment brief.

## Intersection (intersection.py)
Write a python program (intersection.py) which accepts two 􏰄file names (representing graphs) and 􏰄finds the intersection of both graphs. In this context, the intersection refers to set of vertices and edges that are shared by any two graphs. Where an edge is shared but has di􏰃fferent weights in each graph, the weight of the edge in the intersection graph is the larger of the weights. Where an intersection includes a vertex with no edges, that vertex is removed from the intersection. 

Once your program has determined the intersection between two graphs, it should write the resultant graph to a fi􏰄le; this 􏰄file should be named in the following format: graphOne_and_graphTwo.txt so for example if graph G and H were input (from 􏰄files G.txt and H.txt respectively), the resultant graph would be named G_and_H.txt.

## Union (union.py)
Write a python program (union.py) which accepts two 􏰄file names (representing graphs) and 􏰄finds the union of both graphs. In this context, the union refers to set of vertices and edges that are in either of the two graphs. Where an edge is shared but has di􏰃fferent weights in each graph, the weight of the edge in the union graph is the smaller of the weights. 

Once your program has determined the union between two graphs, it should write the resultant graph to a 􏰄file; this 􏰄file should be named in the following format: graphOne_or_graphTwo.txt so for example if graph G and H were input, the resultant graph would be named G_or_H.txt.

## Difference (difference.py)
Write a python program (difference.py) which accepts two 􏰄file names (representing graphs) and fi􏰄nds the di􏰃fference between both graphs. In this context, the di􏰃fference refers to set of edges that are in only one of the two graphs. Where a vertex has no edges in the di􏰃fference it is not included in the resultant graph.

Once your program has determined the diff􏰃erence between two graphs, it should write the resultant graph to a 􏰄file; this 􏰄file should be named in the following format: graphOne_xor_graphTwo.txt so for example if graph G and H were input, the resultant graph would be named G_xor_H.txt.

## Super-graph (supergraph.py)
Write a program (supergraph.py) which accepts three 􏰄file names for diff􏰃erent graphs and, using your work from previous sections, creates a super-graph. In this context a super-graph of N graphs is a graph which includes all of the vertices and edges from all N graphs (using the cheapest edge where edges are shared).

Once you have computed the super-graph for any three graphs you should write it to a 􏰄file; named format: supergraphGraphOne-TwoIntermediateGraphTwo-Three.txt where the graphs are listed in order received but with the intermediary graph in the middle. For example, for the graphs G, H and I we would name the file supergraphGHI.txt. If we received the graphs in a di􏰃fferent order (eg. G, I, H and H, I,G) we would write to a 􏰄file called supergraphGHI.txt and supergraphIHG.txt respectively as H is the intermediate graph. If there is no intermediate graph, you may simply list them in the order received.

## Checking connectivity (connectivity.py)
Now that you have code in place to produce a super-graph, we should con􏰄firm that this super-graph actually does allow the vertices in the base graphs to reach each other via the intermediate graph. Write a program (connectivity.py) which reads in a supergraph (or any combined graph) and determines whether every vertex in this combined graph can reach every other vertex in that graph. If this is possible, you should write to a 􏰄file "graph IS connected", otherwise you should write to a 􏰄file "graph IS NOT connected". In both cases the 􏰄filename should be the 􏰄filename of the combined graph with "connectivity" at the end. For example, given the supergraph GHI as input we would write "graph IS connected" to a fi􏰄le named supergraphGHIconnectivity.txt.

## Greedy approach for cheapest connection (greedy.py)
Write a program (greedy.py) that accepts three graphs as input (via their 􏰄file-names) and follows a greedy approach to determine the cheapest path from the intermediate graph to connect the other two graphs together. As mentioned your program should write to 􏰄files for the resultant graph, the connectivity and path cost. You should name these 􏰄files as:
- greedyGraphOneGraphTwoGraphThree.txt
- greedyGraphOneGraphTwoGraphThreeconnectivity.txt
- greedyGraphOneGraphTwoGraphThreepathCost.txt

In the case of the graphs G, I, and K that would be:
- greedyGKI.txt
- greedyGKIconnectivity.txt
- greedyGKIpathCost.txt

In addition, you should include with your submission a pdf called "greedy.pdf" (you may include an .rtf 􏰄file if you prefer) where you describe what your approach was and why you chose it. Finally, you should also include in your discussion if and where any issues might arise with your application of greed (as greedy algorithms are not guaranteed to yield optimal results for all problems).
