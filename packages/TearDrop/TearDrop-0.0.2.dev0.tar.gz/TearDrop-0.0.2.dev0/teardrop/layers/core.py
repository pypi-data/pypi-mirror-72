from teardrop.core.abstract_classes._abstract_layers import AbstractDenseLayer, AbsRNN
from typing import Union
import numpy as np


class Dense(AbstractDenseLayer):

    """
    A fully connected Dense layer in a basic Neural Network

    Functions
    -----------
    _forward: coroutine
        A function used to count sum of weighted inputs to perform forward propagation.

    _backward: coroutine
        A function used for performing back propagation.

    _initialize: coroutine
        A function initializing weights and biases for the layer.
    """

    def _forward(self, x: Union[list, np.ndarray]) -> np.ndarray:

        """
        Parameters
        -----------
        x: array-like
            Matrix containing data used for model fitting.

        Returns
        --------
        result: array-like
            Matrix after summing all the weighted inputs and performing activation.
        """

        output = super()._forward(x)
        return output

    def _backward(
            self,
            last_derivative: Union[list, np.ndarray],
            lr: Union[int, float],
            optimizer: Union[str]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        last_derivative: array-like
            A matrix containing gradient from the last layer.

        lr: float/int
            Learning rate deciding how big the step of the gradient is.

        optimizer: str
            Optimizer used for optimizing weights and biases.

        Returns
        --------
        last_derivative: array-like
            The derivative passed to the next layer for back propagation.
        """

        last_gradient = super()._backward(last_derivative, lr, optimizer)
        return last_gradient

    def _initialize(
            self,
            neurons: int
    ):

        """
        Parameters
        -----------
        neurons: int
            Number of neurons in layer used to initialize weights.

        Returns
        --------
        None
        """

        super()._initialize(neurons)


class RNN(AbsRNN):
    # TODO: Create an RNN

    """
    RNN layer which can be added to the Sequential model or used independently.

    Functions
    -----------
    _forward
        Function used to perform forward propagation of the layer.

    _backward
        Function used to perform backpropagation on a layer.

    _initialize
        Function which initializes all weights and biases for the layer.
    """

    def _forward(
            self,
            x: Union[np.ndarray, list]
    ) -> np.ndarray:

        """
        Parameters
        ----------
        x: np.ndarray, list
            Layer's input used for forward propagation.


        Returns
        --------
        output: np.ndarray
            Layer's output.
        """

        output = super()._forward(x)
        return output

    def _backward(
            self,
            last_derivative: Union[np.ndarray, list],
            lr: Union[int, float],
            optimizer: str
    ) -> np.ndarray:
        
        """
        
        Parameters
        -----------
        last_derivative: np.ndarray, list
            Gradient from the last layer used to perform backpropagation.
        
        lr: int, float
            Learning rate used to adjust the gradient subtracted from the weights and biases for optimization.
            
        optimizer: str
            Optimizer used for optimizing weights and biases in the layer.
        
        Returns
        --------
        gradient: np.ndarray
            Gradient calculated from this layer passed to the next one for backpropagation.
        """

        gradient = super()._backward(last_derivative, lr, optimizer)
        return gradient
    
    def initialize(
            self,
            cells: int
    ):

        """
        Parameters
        -----------
        cells: int
            Number of cells in layer.
        """

        super().initialize(cells)

    def _name(
            self,
            number: int
    ):
        super()._name(number)
