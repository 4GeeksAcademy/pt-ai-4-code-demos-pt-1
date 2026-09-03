"""Binary Search Tree implementation of an ordered symbol table."""

from __future__ import annotations

from typing import Any, Iterator, Optional


class _Node:
    def __init__(self, key: Any, val: Any) -> None:
        self.key: Any = key
        self.val: Any = val
        self.left: Optional[_Node] = None
        self.right: Optional[_Node] = None


class OrderedSymbolTable:
    """An ordered symbol table backed by a binary search tree."""

    def __init__(self) -> None:
        self._root: Optional[_Node] = None

    def _get(self, x: Optional[_Node], key: Any) -> Any:
        """Return the value for *key* in the subtree rooted at *x*.

        Raises KeyError if not found.
        """
        if x is None:
            raise KeyError(key)
        if key < x.key:
            return self._get(x.left, key)
        if x.key < key:
            return self._get(x.right, key)
        return x.val

    def __getitem__(self, key: Any) -> Any:
        return self._get(self._root, key)

    def _set(self, x: Optional[_Node], key: Any, val: Any) -> _Node:
        """Insert *key* → *val* into the subtree rooted at *x*, returning the new root."""
        if x is None:
            return _Node(key, val)
        if key < x.key:
            x.left = self._set(x.left, key, val)
        elif x.key < key:
            x.right = self._set(x.right, key, val)
        else:
            x.val = val
        return x

    def __setitem__(self, key: Any, val: Any) -> None:
        self._root = self._set(self._root, key, val)

    def _contains(self, x: Optional[_Node], key: Any) -> bool:
        """Return whether *key* exists in the subtree rooted at *x*."""
        if x is None:
            return False
        if key < x.key:
            return self._contains(x.left, key)
        if x.key < key:
            return self._contains(x.right, key)
        return True

    def __contains__(self, key: Any) -> bool:
        return self._contains(self._root, key)

    def _inorder(self, x: Optional[_Node], a: list[Any]) -> None:
        """Append keys from the subtree rooted at *x* to *a* in order."""
        if x is None:
            return
        self._inorder(x.left, a)
        a.append(x.key)
        self._inorder(x.right, a)

    def __iter__(self) -> Iterator[Any]:
        a: list[Any] = []
        self._inorder(self._root, a)
        return iter(a)


def main() -> None:
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