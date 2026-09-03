"""
A collection of graph traversal functions: BFS and DFS.
"""

from collections import deque


def bfs(graph, start):
    """Search through a graph level by level using Breadth-First Search."""
    # Check if the start node is in our graph
    if start not in graph:
        # If not, raise an error to stop the program
        raise KeyError(f"Start node '{start}' not found in graph")

    # Create an empty list to store all the nodes we visit, in order
    visited_nodes = []

    # Create a queue (a line) with the starting node in it
    # A queue is like a line at a store — first person in line gets served first
    queue = deque([start])

    # Create a set to remember which nodes we've already seen
    # A set is like a checklist — we can quickly check if something is on it
    visited_set = {start}

    # Keep looping as long as there are still nodes waiting in the queue
    while queue:
        # Take the first node out of the queue (like serving the first person in line)
        current = queue.popleft()

        # Add this node to our list of visited nodes
        visited_nodes.append(current)

        # Go through each neighbor connected to the current node
        for neighbor in graph[current]:
            # Check if we haven't seen this neighbor before
            if neighbor not in visited_set:
                # Add this neighbor to our checklist so we don't visit it twice
                visited_set.add(neighbor)

                # Put this neighbor at the back of the queue to explore later
                queue.append(neighbor)

    # Send back the list of all nodes we visited
    return visited_nodes


def dfs(graph, start):
    """Search through a graph going deep into each branch using Depth-First Search."""
    # Check if the start node is in our graph
    if start not in graph:
        # If not, raise an error to stop the program
        raise KeyError(f"Start node '{start}' not found in graph")

    # Create an empty list to store all the nodes we visit, in order
    visited_nodes = []

    # Create a stack with the starting node in it
    # A stack is like a pile of plates — the last plate put on top gets taken first
    stack = [start]

    # Create an empty set to remember which nodes we've already seen
    # It's empty because we haven't visited any nodes yet
    visited_set = set()

    # Keep looping as long as there are still nodes waiting in the stack
    while stack:
        # Take the most recently added node off the top of the stack
        # (like taking the top plate off a pile)
        current = stack.pop()

        # Check if we haven't processed this node yet
        if current not in visited_set:
            # Add this node to our checklist so we don't visit it twice
            visited_set.add(current)

            # Add this node to our list of visited nodes
            visited_nodes.append(current)

            # Go through each neighbor of the current node
            # We reverse the list so the first neighbor gets explored first
            for neighbor in reversed(graph[current]):
                # Check if we haven't seen this neighbor before
                if neighbor not in visited_set:
                    # Put this neighbor on top of the stack to explore it soon
                    stack.append(neighbor)

    # Send back the list of all nodes we visited
    return visited_nodes