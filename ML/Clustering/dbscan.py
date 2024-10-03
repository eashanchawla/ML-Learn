"""
Assignment: DBSCAN (Density-Based Spatial Clustering of Applications with Noise)

Implement the DBSCAN clustering algorithm from scratch. DBSCAN groups together points that are closely packed together, marking as outliers points that lie alone in low-density regions.

Steps to implement:
1. Define the DBSCAN class with parameters epsilon (eps) and min_samples
2. Implement the fit method to cluster the data
3. Create helper methods for finding neighbors and expanding clusters
4. Add a predict method to assign new points to clusters or label them as noise

Requirements:
- Use numpy for efficient computations
- Implement proper error handling and input validation
- Provide clear documentation for each method

Bonus:
- Implement a method to visualize the clusters in 2D or 3D
- Add support for different distance metrics (e.g., Euclidean, Manhattan)
"""

import numpy as np

class DBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples

    def fit(self, X):
        # Your implementation here
        pass

    def predict(self, X):
        # Your implementation here
        pass

# Example usage
if __name__ == "__main__":
    # Create sample data and test your DBSCAN implementation
    pass
