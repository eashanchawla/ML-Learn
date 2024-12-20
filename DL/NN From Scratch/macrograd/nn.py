from abc import ABC, abstractmethod
from typing import List
from macrograd.base import Value
import random

class Module(ABC):
    @abstractmethod
    def get_parameters(self) -> List:
        return []

    @abstractmethod
    def zero_grad(self) -> None:
        for param in self.get_parameters():
            param.grad = 0

class Neuron(Module):
    '''Contains weights and biases'''
    def __init__(self, n_inputs: int) -> None:
        self.weights = [Value(random.uniform(-1, 1)) for _ in range(n_inputs)]
        self.bias = Value(random.uniform(-1, 1))

    def __call__(self, x):
        assert len(x) == len(self.weights), f"Expecting input of shape {len(self.weights)} but got {len(x)}"
        act = sum(wi * xi for wi, xi in zip(self.weights, x)) + self.bias
        out = act.tanh()
        return out
    
    def get_parameters(self) -> List:
        return self.weights + [self.bias]
    
    def zero_grad(self):
        return super().zero_grad()
    

class Layer(Module): 
    '''Collection of neurons form a layer in a network'''
    def __init__(self, n_inputs: int, n_outputs: int) -> None:
        '''Define a collection of neurons
        
        Args:
            n_inputs: Number of inputs to each neuron
            n_outputs: Number of outputs i.e. number of neurons since there is 1 output per neuron
        '''
        self.neurons = [Neuron(n_inputs) for _ in range(n_outputs)]
    
    def __call__(self, x):
        outputs = [neuron(x) for neuron in self.neurons]
        return outputs[0] if len(outputs) == 1 else outputs
    
    def get_parameters(self):
        return [param for neuron in self.neurons for param in neuron.get_parameters()]
    
    def zero_grad(self):
        return super().zero_grad()
    
class MLP(Module):
    def __init__(self, n_inputs: float, n_outputs: List[float]):
        n_neurons = [n_inputs] + n_outputs
        self.layers = [Layer(n_neurons[i], n_neurons[i+1]) for i in range(len(n_outputs))]

    def __call__(self, x):
        '''One forward pass through the network with a set of inputs?'''
        for layer in self.layers:
            x = layer(x)
        return x
    
    def get_parameters(self) -> List:
        return [param for layer in self.layers for param in layer.get_parameters()]

    def zero_grad(self):
            return super().zero_grad()