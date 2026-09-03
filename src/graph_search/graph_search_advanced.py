"""
Graph traversal algorithms: Breadth-First Search and Depth-First Search.
"""

from collections import deque


def bfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Traverse a graph using Breadth-First Search.

    Explores all neighbors before moving deeper. Uses a deque for O(1) pops.

    Args:
        graph: Adjacency list. Each key is a node, value is a list of neighbors.
        start: The starting node.

    Returns:
        List of nodes in BFS visitation order.

    Raises:
        KeyError: If start is not in graph.
    """
    if start not in graph:
        raise KeyError(f"Start node '{start}' not found in graph")

    visited_nodes: list[str] = []
    queue: deque[str] = deque([start])
    visited_set: set[str] = {start}

    while queue:
        current = queue.popleft()
        visited_nodes.append(current)
        for neighbor in graph[current]:
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                queue.append(neighbor)

    return visited_nodes


def dfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """
    Traverse a graph using Depth-First Search.

    Explores as far as possible along each branch before backtracking.
    Uses an explicit stack instead of recursion to avoid depth limits.

    Args:
        graph: Adjacency list. Each key is a node, value is a list of neighbors.
        start: The starting node.

    Returns:
        List of nodes in DFS visitation order.

    Raises:
        KeyError: If start is not in graph.
    """
    if start not in graph:
        raise KeyError(f"Start node '{start}' not found in graph")

    visited_nodes: list[str] = []
    stack: list[str] = [start]
    visited_set: set[str] = set()

    while stack:
        current = stack.pop()
        if current not in visited_set:
            visited_set.add(current)
            visited_nodes.append(current)
            for neighbor in reversed(graph[current]):
                if neighbor not in visited_set:
                    stack.append(neighbor)

    return visited_nodes