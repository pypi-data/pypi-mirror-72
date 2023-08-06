from percolation.ds import WeightedQuickUnionUF
from percolation.naive import NaiveDS
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


class Percolation:
    """Percolation.

    This class represents the percolation system of square sites.
    It creates a an n-by-n grid, with all sites initially blocked.

    Args:
        n (int): the size of the grid
        naive (boolean): if naive=True, a worse data structure would be used to generate the system.
    """

    def __init__(self, n, naive=False):
        if naive:
            self.__grid = NaiveDS(n**2+2)
        else:
            self.__grid = WeightedQuickUnionUF(n**2+2)

        self.__is_open = [False] * n**2
        self.__is_full = [False] * n**2
        self.__top = n**2
        self.__bottom = n**2+1
        self.__n = n
        self.__open_sites = 0

    def open(self, row, col):
        """
        Open a site.

        Args:
            row (int): the 1-based index of the row to open.
            col (int): the 1-based index of the column to open.
        """
        neighbors = self.__neighbours(row, col)

        idx = self.__rc_to_index(row, col)

        if self.__is_open[idx]:
            return

        self.__is_open[idx] = True
        self.__open_sites += 1

        if row == 1:
            self.__grid.union(self.__top, idx)
        if row == self.__n:
            self.__grid.union(self.__bottom, idx)

        for n in neighbors:
            if self.__is_open[n]:
                self.__grid.union(idx, n)

    def is_open(self, row, col):
        """
        Checks whether a site is opened.

        Args:
            row (int): the 1-based index of the row to open.
            col (int): the 1-based index of the column to open.

        Returns:
            boolean: whether site is opened.
        """
        idx = self.__rc_to_index(row, col)
        return self.__is_open[idx]

    def is_full(self, row, col):
        """ 
        Checks whether a site is opened. A full site is an open site,
        that can be connected to an open site in the top row via a chain
        of neighboring (left, right, up, down) open sites.

        Args:
            row (int): the 1-based index of the row to open.
            col (int): the 1-based index of the column to open.

        Returns:
            boolean: whether site is full.
        """
        idx = self.__rc_to_index(row, col)
        return self.__is_full[idx]

    def percolates(self):
        """
        Whether a system percolates. We say the system percolates if there is a full site in the bottom row.

        Returns:
            boolean: whether percolates
        """
        return self.__grid.connected(self.__top, self.__bottom)

    def __rc_to_index(self, row, col):
        return (row-1)*self.__n + (col-1)

    def __neighbours(self, row, col):
        up = row - 1
        down = row + 1
        left = col - 1
        right = col + 1

        if up < 1:
            if left < 1:
                return (self.__rc_to_index(down, col), self.__rc_to_index(row, right))
            if right > self.__n:
                return (self.__rc_to_index(down, col), self.__rc_to_index(row, left))

            return self.__rc_to_index(down, col), self.__rc_to_index(row, left), self.__rc_to_index(row, right)

        elif down > self.__n:
            if left < 1:
                return (self.__rc_to_index(up, col), self.__rc_to_index(row, right))
            if right > self.__n:
                return (self.__rc_to_index(up, col), self.__rc_to_index(row, left))

            return self.__rc_to_index(up, col), self.__rc_to_index(row, left), self.__rc_to_index(row, right)

        else:
            if left < 1:
                return (self.__rc_to_index(up, col), self.__rc_to_index(down, col), self.__rc_to_index(row, right))
            if right > self.__n:
                return (self.__rc_to_index(up, col), self.__rc_to_index(down, col), self.__rc_to_index(row, left))

            return self.__rc_to_index(up, col), self.__rc_to_index(down, col), self.__rc_to_index(row, left), self.__rc_to_index(row, right)

    def plot(self):
        """
        Plots the grid.

        Returns:
            matplotlib.pyplot.Figure: the n-by-n grid.
        """
        o1 = np.array(self.__is_open).astype(int)
        o2 = np.reshape(o1, (self.__n, self.__n))

        fig = plt.figure()
        labels = ['Blocked', 'Opened']

        im = plt.imshow(o2, interpolation='none')

        colors = [im.cmap(im.norm(value)) for value in [0, 1]]
        patches = [mpatches.Patch(color=colors[i], label=labels[i])
                   for i in range(2)]
        plt.legend(handles=patches, bbox_to_anchor=(
            1.05, 1), loc=2, borderaxespad=0.)

        return fig
