"""A simple implementation of a Binary Search Tree symbol table."""


class _Node:
    """A single box (node) in our tree that holds one key-value pair."""

    def __init__(self, key, val):
        # The key we use to look things up (like a name)
        self.key = key
        # The value stored alongside the key (like a phone number)
        self.val = val
        # Connection to the left child node (smaller keys go here)
        self.left = None
        # Connection to the right child node (larger keys go here)
        self.right = None


class OrderedSymbolTable:
    """A table that stores key-value pairs and keeps them in sorted order.

    Think of it like a phone book where names are kept in alphabetical order.
    """

    def __init__(self):
        # The topmost node in the tree (None means the tree is empty)
        self._root = None

    def _get(self, x, key):
        """Search for a key starting from node x (helper function)."""
        # If we reached a dead end (None), the key isn't in the tree
        if x is None:
            raise KeyError(key)

        # If the key we're looking for is smaller, go to the left side
        if key < x.key:
            return self._get(x.left, key)

        # If the key we're looking for is larger, go to the right side
        if x.key < key:
            return self._get(x.right, key)

        # If it's not smaller and not larger, it must be equal — found it!
        return x.val

    def __getitem__(self, key):
        """Look up a key using square brackets: st[key]."""
        # Start the search from the very top of the tree
        return self._get(self._root, key)

    def _set(self, x, key, val):
        """Insert a key-value pair starting from node x (helper function)."""
        # If we've found an empty spot, put the new node here
        if x is None:
            return _Node(key, val)

        # If the new key is smaller, go left and keep looking
        if key < x.key:
            x.left = self._set(x.left, key, val)

        # If the new key is larger, go right and keep looking
        elif x.key < key:
            x.right = self._set(x.right, key, val)

        # If the key already exists, just update the value
        else:
            x.val = val

        # Give back the (possibly changed) node
        return x

    def __setitem__(self, key, val):
        """Set a value using square brackets: st[key] = val."""
        # Start the insertion from the top of the tree
        self._root = self._set(self._root, key, val)

    def _contains(self, x, key):
        """Check if a key exists starting from node x (helper function)."""
        # If we hit a dead end, the key is not in the tree
        if x is None:
            return False

        # If the key is smaller, check the left side
        if key < x.key:
            return self._contains(x.left, key)

        # If the key is larger, check the right side
        if x.key < key:
            return self._contains(x.right, key)

        # Keys match — we found it!
        return True

    def __contains__(self, key):
        """Check if a key exists using: key in st."""
        # Start the search from the top of the tree
        return self._contains(self._root, key)

    def _inorder(self, x, a):
        """Collect all keys in sorted order (helper function)."""
        # If we've reached an empty spot, stop going down this path
        if x is None:
            return

        # First, visit everything on the left (smaller keys)
        self._inorder(x.left, a)

        # Then, add the current node's key to our list
        a.append(x.key)

        # Finally, visit everything on the right (larger keys)
        self._inorder(x.right, a)

    def __iter__(self):
        """Loop through all keys in order using: for key in st."""
        # Start with an empty list
        a = []

        # Fill the list with keys in sorted order
        self._inorder(self._root, a)

        # Return an iterator so we can loop over the keys
        return iter(a)


def main():
    """Run a quick demo of the symbol table."""
    from stdio import writeln

    # Create a new empty symbol table
    st = OrderedSymbolTable()

    # Add some names and their values
    st["Sedgewick"] = "Bob"
    st["Wayne"] = "Kevin"
    st["Dondero"] = "Bob"

    # Look up values by their keys
    writeln(st["Sedgewick"])
    writeln(st["Wayne"])
    writeln(st["Dondero"])

    # Check if certain keys exist in the table
    if "Dondero" in st:
        writeln("Dondero found")
    else:
        writeln("Dondero not found")
    if "Kernighan" in st:
        writeln("Kernighan found")
    else:
        writeln("Kernighan not found")

    # Loop through all keys and print each one with its value
    for key in st:
        writeln(f"{key}: {st[key]}")


if __name__ == "__main__":
    # Only run main() when this file is executed directly
    main()