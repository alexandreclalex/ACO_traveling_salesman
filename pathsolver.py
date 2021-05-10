import numpy
import numpy as np
import random
from multiprocessing import Pool

import scipy.spatial.distance


class PathSolver:
    def __init__(self, points, init_pher=10):
        """
        Initializes the Ant Colony Solver
        :param init_pher: initial pheromone levels
        :param points: A (n, 2) array of n pairs of x, y coordinates
        """

        # Initialize Params
        self._points = np.array(points)
        self._pheromones = np.ones((len(points),) * 2)
        self.best_path = np.arange(len(points))
        self.best_dist = self.path_dist(self.best_path)

    def path_dist(self, indices):
        """
        Calculates the length of the path described by indices of points in self._points, plus returning from the
        last point to the first point
        :param indices: Indices of points in order to traverse
        :return: the path distance
        """
        return np.linalg.norm(self._points[indices] - self._points[np.roll(indices, 1)], axis=1).sum()


    def _get_path(self, path):
            path = np.zeros(len(self._points))
            path[0] = int(random.random() * len(self._points))
            for i in range(len(self._points) - 1):
                index = int(path[i])
                distances = scipy.spatial.distance.cdist(self._points, self._points[index, np.newaxis])
                desirability = np.power(1 / numpy.delete(distances, path[:i + 1].astype(int)), self.dist_pow) * \
                               np.power(numpy.delete(self._pheromones[i], path[:i + 1].astype(int)), self.pher_pow)
                path[i + 1], = random.choices(np.delete(np.arange(len(self._points)), path[:i + 1].astype(int)),
                                              weights=desirability, k=1)
            return path
            

    def run_1_iteration(self, num_ants, dist_pow, pher_pow, pher_intensity, dissipation):
        paths = np.zeros((num_ants, len(self._points)))
        self.dist_pow = dist_pow
        self.pher_pow = pher_pow
        
        with Pool(8) as p:
            map_proc = p.map_async(self._get_path, paths)
            paths = np.array(map_proc.get())

        paths = paths.astype(int)


        distances = np.array([self.path_dist(path) for path in paths])
        best = min(distances)
        if best < self.best_dist:
            self.best_path = paths[distances.argmin()]
            self.best_dist = best

        self._pheromones = self._pheromones * (1 - dissipation)

        for path_index in range(len(paths)):
            path = paths[path_index]
            for i in range(len(path) - 1):
                self._pheromones[path[i], path[i + 1]] += pher_intensity / distances[path_index]
            self._pheromones[path[0], path[-1]] += pher_intensity / distances[path_index]

    def get_pheromones(self):
        return self._pheromones.copy()


if __name__ == '__main__':
    points = np.random.randint(0, 1000, (100, 2))
    s = PathSolver(points, 2)
    s.run_1_iteration(10, 2, 2, 10, 0.3)
