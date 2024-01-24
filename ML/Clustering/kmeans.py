'''
Kmeans algo
1. Choose initial centroids
2. Asign points to clusters
3. Update the centroids by taking the mean of all points in the cluster
4. Repeat Steps 2-4 till difference between the old and new centroids is above a certain threshold i.e. till changes are big

Edge cases:
1. What if there are no points
2. What if n_clusters > data points in the dataset
3. If we reach that stopping condition of threshold, should we still update centroids or not? 
'''

import random
import numpy as np
import pandas as pd
from typing import List

class KMeans:
    def __init__(self, n_clusters=3, threshold=2, max_iterations=100) -> None:
        self.n_clusters=n_clusters
        self.threshold=threshold
        self.max_iterations=max_iterations
        self.centroids=None

    def initialize_clusters(self, X):
        return X[np.random.choice(X.shape[0], size=self.n_clusters, replace=False)]
        # return np.random.sample(X, self.n_clusters)

    def calculate_distance(self, a: List[float], b: List[float]) -> float:
        sd = [(x-y)**2 for x,y in zip(a,b)]
        return np.sqrt(np.sum(sd))

    def assign_cluster(self, point, centroids):
        min_index, min_distance = 0, np.inf
        for i, centroid in enumerate(centroids):
            calculated_distance = self.calculate_distance(point, centroid)
            if min_distance > calculated_distance:
                min_distance=calculated_distance
                min_index=i
        return min_index
    
    def assign_points_to_clusters(self, X: np.array, centroids: np.array):
        cluster_assignments=list()
        for point in X:
            cluster_assignments.append(self.assign_cluster(point, centroids))
        return cluster_assignments

    def update_clusters(self, X, cluster_assignments):
        new_centroids=[]
        for cluster_number in range(self.n_clusters):
            subset = [X[i] for i in range(len(X)) if cluster_number==cluster_assignments[i]]
            if subset:
                new_centroids.append(np.mean(subset, axis=0))
            else:
                new_centroids.append(self.centroids[cluster_number])
        return new_centroids


    def fit(self, X):
        self.centroids = self.initialize_clusters(X)
        for i in range(self.max_iterations):
            cluster_assignments = self.assign_points_to_clusters(X, self.centroids)
            centroids = self.update_clusters(X, cluster_assignments)
            max_centroid_change = max([self.calculate_distance(self.centroids[cluster_number], centroids[cluster_number]) for cluster_number in range(self.n_clusters)])
            if max_centroid_change < self.threshold:
                break
            self.centroids = centroids
            
        if i!=self.max_iterations-1:
            print(f'Early stopping: {i}')

    def transform(self):
        pass

    def fit_transform(self):
        self.centroids = self.initialize_clusters(X)
        for i in range(self.max_iterations):
            cluster_assignments = self.assign_points_to_clusters(X, self.centroids)
            centroids = self.update_clusters(X, cluster_assignments)
            max_centroid_change = max([self.calculate_distance(self.centroids[cluster_number], centroids[cluster_number]) for cluster_number in range(self.n_clusters)])
            self.centroids = centroids
            if max_centroid_change < self.threshold:
                break
            
        if i!=self.max_iterations-1:
            print(f'Early stopping: {i}')
        return cluster_assignments


class FastKMeans(KMeans):
    def __init__(self, n_clusters=3, threshold=2, max_iterations=100) -> None:
        super().__init__(n_clusters, threshold, max_iterations)

    def initialize_clusters(self, X):
        pass
