'''
KMeans Algorithm:
1. Initialize cluster centroids
2. Based on cluster centroids, assign each point to a cluster
3. Re-calculate cluster centroids based on new set of points
4. Repeat steps 2-4 till stopping criteria is met

Edge cases:
1. What if there are no points (Handled)
2. What if n_clusters > data points in the dataset (handled)
3. If we reach that stopping condition of threshold, should we still update centroids or not? (handled)
'''
import numpy as np
from tqdm import tqdm

class KMeans:
    def __init__(self, n_clusters=2, max_iterations=100, distance_threshold=0.1) -> None:
        if n_clusters <= 0:
            # by this logic I should throw errors or warnings for the other parameters as well dude
            raise ValueError("Number of clusters must be greater than 0")
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.distance_threshold = distance_threshold
        self.cluster_centroids = None

    def dooriyan(self, a: np.array, b: np.array):
        '''Calculate euclidean distance between 2 points in an n-dimensional space'''
        if a.shape[0]!=b.shape[0]:
            raise ValueError(f'Dimensions of 2 points not matching: {a}; {b}.')
        
        sum_squared_dist = [(x-y)**2 for x, y in zip(a, b)]
        return np.sqrt(np.sum(sum_squared_dist))

    def calculate_centroids(self, X: np.array, assignments: np.array=None) -> np.array:
        '''Random initialization of clusters'''
        if self.cluster_centroids is None:
            selected_indices = np.random.choice(X.shape[0], size=self.n_clusters, replace=False)
            return X[selected_indices]
        
        new_cluster_centroids = []
        for current_cluster_index in range(self.n_clusters):
            subset = [X[i] for i in range(len(assignments)) if assignments[i]==current_cluster_index]
            if subset:
                new_cluster_centroids.append(np.mean(subset, axis=0))
            else:
                new_cluster_centroids.append(self.cluster_centroids[current_cluster_index])

        if len(new_cluster_centroids) != self.n_clusters:
            raise ValueError("Centroids genereated != Number of clusters specified")
        return np.array(new_cluster_centroids)
    
    def assign_point(self, point):
        min_distance = np.inf
        min_cluster_index = -1
        for i, centroid in enumerate(self.cluster_centroids):
            dist = self.dooriyan(point, centroid)
            if dist < min_distance:
                # what if the distance is equal? | currently we just don't change if the distance is same
                min_cluster_index = i
                min_distance = dist
        if min_cluster_index == -1:
            raise Warning('Why did we run into this case buddy? Min clust dist stayed -1 till the end')
        return min_cluster_index
        
    def assign_clusters(self, X: np.array) -> np.array:
        cluster_assignments = list()
        for current_point in X:
            cluster_assignments.append(self.assign_point(current_point))
        return cluster_assignments
            
    
    def sikhao(self, X):
        '''Fit/Sikhao'''
        if self.n_clusters > X.shape[0]:
            raise ValueError("Number of clusters cannot exceed the number of points")
        self.cluster_centroids = self.calculate_centroids(X=X)
        average_change = np.inf
        for i in tqdm(range(self.max_iterations)):
            cluster_assignments=self.assign_clusters(X)
            new_cluster_centroids = self.calculate_centroids(X, cluster_assignments)
            average_change = np.average([self.dooriyan(a, b) for a, b in zip(self.cluster_centroids, new_cluster_centroids)])
            if average_change <= self.distance_threshold:
                break
            self.cluster_centroids = new_cluster_centroids
        if i != self.max_iterations:
            print(f'Early stopping due to distance condition')

        
    def batao(self, X):
        '''Predict/Batao'''
        return self.assign_clusters(X)

    def sikhao_aur_batao(self, X):
        '''Fit and predict / Sikhao aur batao'''
        self.sikhao(X)
        return self.batao(X)

