"""
Assignment: Decision Tree

Implement a decision tree algorithm from scratch. Decision trees can be used for both classification and regression tasks.

Steps to implement:
1. Define the DecisionTree class with parameters like max_depth, min_samples_split
2. Implement the fit method to build the tree recursively
3. Create helper methods for calculating information gain or Gini impurity
4. Add a predict method to make predictions on new data

Requirements:
- Use numpy for efficient computations
- Implement proper error handling and input validation
- Provide clear documentation for each method
- Support both classification and regression tasks

Bonus:
- Implement pruning to prevent overfitting
- Add support for continuous and categorical features
"""

import numpy as np

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, task='classification'):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.task = task
        self.tree = None

    def fit(self, X, y):
        # Your implementation here
        pass

    def predict(self, X):
        # Your implementation here
        pass

# Example usage
if __name__ == "__main__":
    # Create sample data and test your Decision Tree implementation
    pass
