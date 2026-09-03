class OrderedSymbolTable:

    def __init__(self):
        self._root = None

    def _get(self, x, key):
        if x is None:
            raise KeyError
        if key < x.key:
            return self._get(x.left, key)
        elif x.key < key:
            return self._get(x.right, key)
        else:
            return x.val

    def __getitem__(self, key):
        return self._get(self._root, key)

    def _set(self, x, key, val):
        if x is None:
            return _Node(key, val)
        if key < x.key:
            x.left = self._set(x.left, key, val)
        elif x.key < key:
            x.right = self._set(x.right, key, val)
        else:
            x.val = val
        return x

    def __setitem__(self, key, val):
        self._root = self._set(self._root, key, val)

    def _contains(self, x, key):
        if x is None:
            return False
        if key < x.key:
            return self._contains(x.left, key)
        if x.key < key:
            return self._contains(x.right, key)
        return True

    def __contains__(self, key):
        return self._contains(self._root, key)

    def _inorder(self, x, a):
        if x is None:
            return
        self._inorder(x.left, a)
        a += [x.key]
        self._inorder(x.right, a)

    def __iter__(self):
        a = []
        self._inorder(self._root, a)
        return iter(a)


class _Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None


def main():

    import stdio

    st = OrderedSymbolTable()

    st['Sedgewick'] = 'Bob'
    st['Wayne'] = 'Kevin'
    st['Dondero'] = 'Bob'

    stdio.writeln(st['Sedgewick'])
    stdio.writeln(st['Wayne'])
    stdio.writeln(st['Dondero'])

    if 'Dondero' in st:
        stdio.writeln('Dondero found')
    else:
        stdio.writeln('Dondero not found')
    if 'Kernighan' in st:
        stdio.writeln('Kernighan found')
    else:
        stdio.writeln('Kernighan not found')

    for key in st:
        stdio.writeln(key + ': ' + st[key])


if __name__ == '__main__':
    main()