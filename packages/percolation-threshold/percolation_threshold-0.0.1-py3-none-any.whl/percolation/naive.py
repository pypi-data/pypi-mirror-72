class NaiveDS():
    """
    (DEPRECEATED) Naive way to create a Union find data structure.
    You should be using this, this was added only for comparaison
    with the WeightedQuickUnionUF.

    Args:
        n (int): number of elements.
    """

    def __init__(self, N):
        self.N = N
        self.cnxed = []

    def connected(self, a, b):
        """
        Checks whether two elements are connected.

        Args:
            p (int): element
            q (int): element

        Returns:
            boolean: whether two elements are connected
        """
        for i in self.cnxed:
            if a in i and b in i:
                return True
        return False

    def union(self, a, b):
        """
        Unite two elements.

        Args:
            p (int): element
            q (int): element
        """

        a_index = None
        b_index = None

        for i in range(len(self.cnxed)):
            if a in self.cnxed[i]:
                a_index = i
            if b in self.cnxed[i]:
                b_index = i

        if a_index is None and b_index is None:
            self.cnxed.append(set([a, b]))
        elif a_index is not None and b_index is None:
            self.cnxed[a_index] = set([b, *self.cnxed[a_index]])
        elif a_index is None and b_index is not None:
            self.cnxed[b_index] = set([a, *self.cnxed[b_index]])
        else:
            self.cnxed[a_index] = set(
                [*self.cnxed[a_index], *self.cnxed[b_index]])
            self.cnxed.remove(self.cnxed[b_index])
