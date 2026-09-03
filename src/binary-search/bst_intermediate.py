"""Binary Search Tree implementation of an ordered symbol table."""


class _Node:
    """A single node in the binary search tree."""

    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None


class OrderedSymbolTable:
    """An ordered symbol table backed by a binary search tree."""

    def __init__(self):
        self._root = None

    def _get(self, x, key):
        """Search for a key in the subtree, returning its value."""
        # Base case: reached an empty subtree — key not found
        if x is None:
            raise KeyError(key)

        # Decide which side of the tree to search based on comparison
        if key < x.key:
            return self._get(x.left, key)
        if x.key < key:
            return self._get(x.right, key)

        # Keys are equal — found the matching node
        return x.val

    def __getitem__(self, key):
        """Look up a key starting from the root."""
        return self._get(self._root, key)

    def _set(self, x, key, val):
        """Insert or update a key-value pair in the subtree."""
        # Reached an empty spot — insert a new node here
        if x is None:
            return _Node(key, val)

        # Navigate left or right depending on the key comparison
        if key < x.key:
            x.left = self._set(x.left, key, val)
        elif x.key < key:
            x.right = self._set(x.right, key, val)
        else:
            # Keys match — update the existing value
            x.val = val
        return x

    def __setitem__(self, key, val):
        """Insert a key-value pair starting from the root."""
        self._root = self._set(self._root, key, val)

    def _contains(self, x, key):
        """Check if a key exists in the subtree."""
        # Reached an empty subtree without finding the key
        if x is None:
            return False

        # Search left or right depending on key comparison
        if key < x.key:
            return self._contains(x.left, key)
        if x.key < key:
            return self._contains(x.right, key)

        # Found the matching key
        return True

    def __contains__(self, key):
        """Check if a key exists in the table."""
        return self._contains(self._root, key)

    def _inorder(self, x, a):
        """Collect keys in sorted order via in-order traversal."""
        # Visit left subtree, then this node, then right subtree
        if x is None:
            return
        self._inorder(x.left, a)
        a.append(x.key)
        self._inorder(x.right, a)

    def __iter__(self):
        """Iterate over all keys in ascending order."""
        a = []
        self._inorder(self._root, a)
        return iter(a)


def main():
    from stdio import writeln

    st = OrderedSymbolTable()

    st["Sedgewick"] = "Bob"
    st["Wayne"] = "Kevin"
    st["Dondero"] = "Bob"

    writeln(st["Sedgewick"])
    writeln(st["Wayne"])
    writeln(st["Dondero"])

    if "Dondero" in st:
        writeln("Dondero found")
    else:
        writeln("Dondero not found")
    if "Kernighan" in st:
        writeln("Kernighan found")
    else:
        writeln("Kernighan not found")

    for key in st:
        writeln(f"{key}: {st[key]}")


if __name__ == "__main__":
    main()