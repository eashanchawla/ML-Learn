"""
Assignment: Linear Regression

Implement a simple linear regression algorithm from scratch. Linear regression is used to model the relationship between a dependent variable and one or more independent variables.

Steps to implement:
1. Define the LinearRegression class
2. Implement the fit method to train the model using ordinary least squares
3. Create a predict method to make predictions on new data
4. Add methods to calculate R-squared and Mean Squared Error (MSE)

Requirements:
- Use numpy for efficient computations
- Implement proper error handling and input validation
- Provide clear documentation for each method

Bonus:
- Implement a method to visualize the regression line (for simple linear regression)
- Add support for multiple linear regression
"""

import numpy as np

class LinearRegression:
    def __init__(self):
        self.coefficients = None
        self.intercept = None

    def fit(self, X, y):
        # Your implementation here
        pass

    def predict(self, X):
        # Your implementation here
        pass

    def r_squared(self, X, y):
        # Your implementation here
        pass

    def mse(self, X, y):
        # Your implementation here
        pass

# Example usage
if __name__ == "__main__":
    # Create sample data and test your Linear Regression implementation
    pass
