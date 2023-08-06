class WeightedQuickUnionUF:
    """
    WeightedQuickUnionUF.

    A simple implementation of the disjoint-set data structure.
    https://en.wikipedia.org/wiki/Disjoint-set_data_structure

    Args:
        n (int): number of elements.
    """

    def __init__(self, n):
        self.__arr = list(range(n))
        self.__sz = [1]*n
        self.__n = n

    def __find_root(self, p):
        while p != self.__arr[p]:
            self.__arr[p] = self.__arr[self.__arr[p]]
            p = self.__arr[p]

        return p

    def connected(self, p, q):
        """
        Checks whether two elements are connected.

        Args:
            p (int): element
            q (int): element

        Returns:
            boolean: whether two elements are connected
        """
        self.__validate(p)
        self.__validate(q)

        return self.__find_root(p) == self.__find_root(q)

    def union(self, p, q):
        """
        Unite two elements.

        Args:
            p (int): element
            q (int): element
        """
        self.__validate(p)
        self.__validate(q)

        r_p = self.__find_root(p)
        r_q = self.__find_root(q)

        if r_p == r_q:
            return

        if self.__sz[r_p] < self.__sz[r_q]:
            self.__arr[r_p] = r_q
            self.__sz[r_q] += self.__sz[r_p]
        else:
            self.__arr[r_q] = r_p
            self.__sz[r_p] += self.__sz[r_q]

    def __validate(self, i):
        if i >= self.__n or i < 0 or not isinstance(i, int):
            raise Exception("Illegal argument!")
