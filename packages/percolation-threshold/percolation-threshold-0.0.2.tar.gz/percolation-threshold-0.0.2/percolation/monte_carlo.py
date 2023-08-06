from percolation.grid import Percolation
import numpy as np
import multiprocessing
import psutil


class PercolationMonteCarlo:
    """
    Performs a series of computational experiments, to deduce the percolation threshold.

    Args:
        n (int): the size of the grid.
        trials (int): number of monte carlo experiments to run.
        multiprocess (boolean): whether to use multiprocessing to generate results.

    Attributes:
        results (numpy.array): Stores the results of the experiments (number of opened sites till percolations).

    """

    def __init__(self, n, trials, multiprocess=True):
        self.__trials = trials
        self.__n = n

        if multiprocess:
            results = []
            n_processes = psutil.cpu_count(logical=True)
            trial_process = trials // n_processes
            trial_left = trials % n_processes

            pool = multiprocessing.Pool(processes=n_processes)

            pool_jobs = []
            for i in range(n_processes):
                if i == 0:
                    n_procs = trial_process + trial_left
                else:
                    n_procs = trial_process

                job = pool.apply_async(self.run, (n_procs,))
                pool_jobs.append(job)

            for i, job in enumerate(pool_jobs):
                results.append(job.get())

            self.results = np.array(results)

        else:
            self.results = np.zeros(trials, dtype=np.float64)

            for i in range(trials):
                p = Percolation(self.__n)
                for j in range(self.__n**2):
                    row = np.random.randint(self.__n)+1
                    col = np.random.randint(self.__n)+1

                    while p.is_open(row, col):
                        row = np.random.randint(self.__n)+1
                        col = np.random.randint(self.__n)+1

                    p.open(row, col)

                    if p.percolates():
                        self.results[i] = (j+1)/(self.__n**2)
                        break

    def run(self, trials):
        """
        (Deprecated) Runs n experiments. Preferrably create a PercolationMonteCarlo, it will run experiments automatically.

        Args:
            trials (int): number of monte carlo experiments to run.
        """
        np.random.seed()
        for i in range(trials):
            p = Percolation(self.__n)
            for j in range(self.__n**2):
                row = np.random.randint(self.__n)+1
                col = np.random.randint(self.__n)+1

                while p.is_open(row, col):
                    row = np.random.randint(self.__n)+1
                    col = np.random.randint(self.__n)+1

                p.open(row, col)

                if p.percolates():
                    return (j+1)/(self.__n**2)

    def mean(self):
        """
        Calculate the cross correlation of array b against array a.

        Args:
            a (array): numpy vector. Reference against which cross
                correlation is calculated.
            b (array): numpy vector. The resulting cross-correlation function
                will show how b should be shifted to line up with vector a.

        Returns:
            array: cross-correlation function
        """
        return np.mean(self.results)

    def std(self):
        """
        Calculate the cross correlation of array b against array a.

        Args:
            a (array): numpy vector. Reference against which cross
                correlation is calculated.
            b (array): numpy vector. The resulting cross-correlation function
                will show how b should be shifted to line up with vector a.

        Returns:
            array: cross-correlation function
        """
        return np.std(self.results, ddof=1)

    def confidenceLo(self):
        """
        Calculate the cross correlation of array b against array a.

        Args:
            a (array): numpy vector. Reference against which cross
                correlation is calculated.
            b (array): numpy vector. The resulting cross-correlation function
                will show how b should be shifted to line up with vector a.

        Returns:
            array: cross-correlation function
        """
        return self.mean() - (1.96 * self.std() / np.sqrt(self.__trials))

    def confidenceHi(self):
        """
        Calculate the cross correlation of array b against array a.

        Args:
            a (array): numpy vector. Reference against which cross
                correlation is calculated.
            b (array): numpy vector. The resulting cross-correlation function
                will show how b should be shifted to line up with vector a.

        Returns:
            array: cross-correlation function
        """
        return self.mean() + (1.96 * self.std() / np.sqrt(self.__trials))

    def __repr__(self):
        res = f"Mean\t\t\t {self.mean()}\nStandard Deviation\t {self.std()}\n95% Confidence Interval\t [{self.confidenceLo()}, {self.confidenceHi()}]\n"

        return res
