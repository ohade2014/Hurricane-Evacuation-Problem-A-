# Hurricane-Evacuation-Problem-A*-
Using Artificial Intelligence algorithms, A*, A* real-time for solving. wrote in Python.
- We are given a weighted graph, and the goal is (starting at a given vertex) to visit as many as possible out of a set of vertices, and reach given goal vertices before a given deadline. However, unlike standard shortest path problems in graphs, which have easy known efficient solution methods (e.g. the Dijkstra algorithm), here the problem is that there are more than 2 vertices to visit, their order is not given, and even the number of visited vertices is not known in advance. This is a problem encountered in many real-world settings, such as when you are trying to evacuate people who are stuck at home with no transportation before the hurricane arrives.
- I use heuristic evaluation function (the logic behind the function is detailed in the attached document).
- There are 3 kinds of agents:
 
 -A greedy search agent, that picks the move with best immediate heuristic value to expand next.
 
 -An agent using A* search, with the same heuristic. Assuming a global constant of LIMIT expansions (default 100000) beyond which we just return "fail", and the agent does just the "terminate" action.
 
 -An agent using a simplified version of real-time A* doing L (user determined constant, L=10 by default) expansions before each move decision.
