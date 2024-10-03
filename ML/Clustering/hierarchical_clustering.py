"""
Assignment: Hierarchical Clustering

Implement the Hierarchical Clustering algorithm from scratch. This algorithm builds a hierarchy of clusters, either using a bottom-up (agglomerative) or top-down (divisive) approach.

Steps to implement:
1. Define the HierarchicalClustering class with parameters like linkage type and number of clusters
2. Implement the fit method to build the cluster hierarchy
3. Create helper methods for calculating distances between clusters based on the chosen linkage
4. Add a method to cut the dendrogram at a specified number of clusters

Requirements:
- Use numpy for efficient computations
- Implement at least two linkage methods (e.g., single, complete, average)
- Provide clear documentation for each method

Bonus:
- Implement a method to visualize the dendrogram
- Add support for different distance metrics (e.g., Euclidean, Manhattan)
"""

import numpy as np

class HierarchicalClustering:
    def __init__(self, n_clusters, linkage='single'):
        self.n_clusters = n_clusters
        self.linkage = linkage

    def fit(self, X):
        # Your implementation here
        pass

    def predict(self, X):
        # Your implementation here
        pass

# Example usage
if __name__ == "__main__":
    # Create sample data and test your Hierarchical Clustering implementation
    pass
