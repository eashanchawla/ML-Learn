from typing import Tuple, Optional
from __future__ import annotations
import math

class Value:
    '''Lowest unit of this activity. Represents a value, on which we will do operations, differentiation etc.
       I need to keep track of: Value, operation that created it, parents that led to its creation, differentiation function?
    '''
    def __init__(self, data: float, name: Optional[str] = '', _op: str = None, _parents: Tuple['Value'] = ()) -> None:
        self.data = data
        self._backward = lambda : None
        self._op = _op
        self._parents = _parents
        self.name = name
        self.grad = 0.0

    def __repr__(self) -> str:
        '''way to recreate the value object, meant for developers'''
        return f'Value(data={self.data}, name={self.name}, op={self._op})'

    def __add__(self, other: Value) -> Value:
        '''a+b, where a and b are Value objects, a.__add__(b) called'''
        if isinstance(other, (int, float)):
            other = Value(other)
        out = Value(self.data + other.data, _op='+', _parents=(self, other))
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out
        
    def __mul__(self, other: Value) -> Value:
        '''a*b, where a and b are Value objects, a.__mul__(b) called'''
        if isinstance(other, (int, float)):
            other = Value(other)
        
        out = Value(self.data * other.data, _op='*', _parents=(self, other))
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    
    def __rmul__(self, other):
        '''when b*a called, where b is a scalar, a.__rmul__(b) called.'''
        return self * other
    
    def __radd__(self, other):
        '''when b+a called, where b is a scalar, a.__radd__(b) called.'''
        return self + other
    
    def __pow__(self, other: float):
        '''when we call a ** b, a.__pow__(b) is called, where b is a scalar.'''
        if not isinstance(other, (int, float)):
            raise ValueError("Trying to calculate exp on an incompatible data type. Only supporting int and float.")
        out = Value(self.data ** other, _op=f'**{other}', _parents=(self, ))
        def _backward():
            self.grad += other * (self.data ** (other -1)) * out.grad
        out._backward = _backward
        return out
    
    def tanh(self):
        x = (2 * self).exp()
        out = (x - 1) / (x + 1)
        return out
    
    def exp(self):
        '''calling exponent on a.exp() is equivalent to e raised to a'''
        out = Value(math.exp(self.data), _op='exp', _parents=(self, ))
        def _backward():
            self.grad += math.exp(self.data) * out.grad
        out._backward = _backward
        return out
        
    def __truediv__(self, other):
        '''when we call a / b on 2 value objects, a.__truediv__(b) is called.'''
        out = self * (other ** -1)
        return out
    
    def __neg__(self):
        return self * -1
    
    def __sub__(self, other):
        return self + (-other)

    def backward(self):
        ordering = []
        visited = []
        def topological_traversal(e):
            if e not in visited:
                visited.append(e)
                if e._parents:
                    for parent in e._parents:
                        topological_traversal(parent)
                ordering.append(e)
        topological_traversal(self)
        self.grad = 1.0
        for node in reversed(ordering):
            node._backward()