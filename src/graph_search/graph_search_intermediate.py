"""
Graph traversal algorithms: BFS and DFS.
"""

from collections import deque


def bfs(graph, start):
    """Traverse a graph using Breadth-First Search."""
    # Make sure the start node exists in the graph
    if start not in graph:
        raise KeyError(f"Start node '{start}' not found in graph")

    # Track nodes in the order we visit them
    visited_nodes = []

    # Use a queue to decide which node to explore next
    # (FIFO — first in, first out)
    queue = deque([start])

    # Keep a set of nodes we've already seen to avoid revisiting
    visited_set = {start}

    # Keep going until there are no more nodes to explore
    while queue:
        # Take the next node from the front of the queue
        current = queue.popleft()
        visited_nodes.append(current)

        # Look at all neighbors of the current node
        for neighbor in graph[current]:
            # If we haven't seen this neighbor yet, add it to the queue
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)

    return visited_nodes


def dfs(graph, start):
    """Traverse a graph using Depth-First Search."""
    # Make sure the start node exists in the graph
    if start not in graph:
        raise KeyError(f"Start node '{start}' not found in graph")

    # Track nodes in the order we visit them
    visited_nodes = []

    # Use a stack to decide which node to explore next
    # (LIFO — last in, first out — explores depth first)
    stack = [start]

    # Keep a set of nodes we've already seen to avoid revisiting
    visited_set = set()

    # Keep going until there are no more nodes to explore
    while stack:
        # Take the most recently added node from the stack
        current = stack.pop()

        # Only process this node if we haven't already
        if current not in visited_set:
            visited_set.add(current)
            visited_nodes.append(current)

            # Add all unvisited neighbors to the stack
            # Reversing keeps the first neighbor explored first
            for neighbor in reversed(graph[current]):
                if neighbor not in visited_set:
                    stack.append(neighbor)

    return visited_nodes