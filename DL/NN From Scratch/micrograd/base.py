from typing import Optional, Tuple
from __future__ import annotations

class Value:
    '''Lowest unit of this activity. Represents a value, on which we will do operations, differentiation etc.
       I need to keep track of: Value, operation that created it, parents that led to its creation, differentiation function?
    '''
    def __init__(self, data: float, name: Optional[str] = None, _op: str = None, _parents: Tuple['Value'] = ()) -> None:
        self.data = data
        self._backward = lambda : None
        self._op = _op
        self._parents = _parents
        self.name = name
        self.grad = 0

    def __repr__(self) -> str:
        return f'Value(data={self.data}, name={self.name}, op={self._op})'

    def __add__(self, other: Value) -> Value:
        out = Value(self.data + other.data, _op='+', _parents=(self, other))
        def _backward():
            self.grad = 1.0 * out.grad
            other.grad = 1.0 * out.grad
        out._backward = _backward
        return out
        
    def __mul__(self, other: Value) -> Value:
        out = Value(self.data * other.data, _op='*', _parents=(self, other))
        def _backward():
            self.grad = other.data * out.grad
            other.grad = self.data * out.grad
        out._backward = _backward
        return out
    
    def __rmul__(self, other):
        return other * self
    
    def __exp__(self, other):
        raise NotImplementedError
    
    def tanh(self, other):
        raise NotImplementedError
    
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

        for node in reversed(ordering):
            node._backward()