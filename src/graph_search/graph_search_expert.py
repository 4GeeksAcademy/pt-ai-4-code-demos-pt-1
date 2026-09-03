"""
Graph traversal algorithms: Breadth-First Search and Depth-First Search.

This module provides implementations of BFS and DFS for graphs represented
as adjacency lists. Both algorithms are implemented iteratively to avoid
recursion-depth limits on large graphs.

Typical usage example:

    >>> graph = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []}
    >>> bfs(graph, "A")
    ['A', 'B', 'C', 'D', 'E']
    >>> dfs(graph, "A")
    ['A', 'B', 'D', 'C', 'E']
"""

from collections import deque


def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Traverse a graph using Breadth-First Search, returning nodes in visitation order.

    BFS explores all neighbors of a node before moving to the next level of the graph.
    This implementation uses a double-ended queue (deque) for O(1) pops from the front,
    and a set for O(1) membership checks.

    Args:
        graph: An adjacency list representation of the graph. Each key is a node,
               and its value is a list of neighboring nodes. All nodes must appear
               as keys, even if they have no outgoing edges.
        start: The node from which to begin the traversal. Must be a key in `graph`.

    Returns:
        A list of node names in the order they were first visited by the BFS traversal.

    Raises:
        KeyError: If `start` is not a key in `graph`.

    Example:
        >>> graph = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []}
        >>> bfs(graph, "A")
        ['A', 'B', 'C', 'D', 'E']

    Notes:
        BFS is ideal for finding the shortest path in unweighted graphs because
        it explores nodes in order of their distance from the start node.
    """
    if start not in graph:
        raise KeyError(f"Start node '{start}' not found in graph")

    visited_nodes: list[str] = []
    queue: deque[str] = deque([start])
    visited_set: set[str] = {start}

    while queue:
        current: str = queue.popleft()
        visited_nodes.append(current)

        for neighbor in graph[current]:
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)

    return visited_nodes


def dfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Traverse a graph using Depth-First Search, returning nodes in visitation order.

    DFS explores as far as possible along each branch before backtracking.
    This implementation uses an explicit stack (list) rather than recursion
    to avoid Python's recursion-depth limit on deep or wide graphs.

    Args:
        graph: An adjacency list representation of the graph. Each key is a node,
               and its value is a list of neighboring nodes. All nodes must appear
               as keys, even if they have no outgoing edges.
        start: The node from which to begin the traversal. Must be a key in `graph`.

    Returns:
        A list of node names in the order they were first visited by the DFS traversal.

    Raises:
        KeyError: If `start` is not a key in `graph`.

    Example:
        >>> graph = {"A": ["B", "C"], "B": ["D"], "C": ["E"], "D": [], "E": []}
        >>> dfs(graph, "A")
        ['A', 'B', 'D', 'C', 'E']

    Notes:
        Unlike BFS, DFS does not guarantee shortest paths. However, it uses
        less memory on wide graphs since the stack only holds one branch at a time.
    """
    if start not in graph:
        raise KeyError(f"Start node '{start}' not found in graph")

    visited_nodes: list[str] = []
    stack: list[str] = [start]
    visited_set: set[str] = set()

    while stack:
        current: str = stack.pop()

        if current not in visited_set:
            visited_set.add(current)
            visited_nodes.append(current)

            for neighbor in reversed(graph[current]):
                if neighbor not in visited_set:
                    stack.append(neighbor)

    return visited_nodes