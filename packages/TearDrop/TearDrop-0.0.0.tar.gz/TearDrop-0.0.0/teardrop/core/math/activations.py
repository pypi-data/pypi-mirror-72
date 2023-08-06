import teardrop.core.abstract_classes._abstract_activation as activations
from typing import Union
import numpy as np


class Sigmoid(activations.AbstractSigmoid):
    def activate(
            self,
            x: Union[np.ndarray, int, float]
    ):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        activated: array-like/int/float
            Matrix after performing activation on it.
        """

        activated = super().activate(x)
        return activated

    def gradient(
            self,
            x: Union[np.ndarray, int, float]
    ):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        result: array-like/int/float
            Matrix after performing gradient on it.
        """

        next_gradient = super().gradient(x)
        return next_gradient


class Relu(activations.AbstractRelu):
    def activate(
            self,
            x: Union[np.ndarray, int, float]
    ):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        activated_input: array-like/int/float
            Matrix after performing activation on it.
        """

        activated_input = super().activate(x)
        return activated_input

    def gradient(self, x):

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        result: array-like/int/float
            Matrix after performing gradient on it.
        """

        next_gradient = super().activate(x)
        return next_gradient


class Softmax(activations.AbstractSigmoid):

    def activate(
            self,
            x: Union[list, np.ndarray]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        activated: array-like/int/float
            Matrix after performing activation on it.
        """

        activated = super().activate(x)
        return activated

    def gradient(
            self,
            x: Union[list, np.ndarray]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        x: array-like/int/float
            Matrix of summed weighted sums which have to be activated.

        Returns
        --------
        result: array-like/int/float
            Matrix after performing gradient on it.
        """

        next_gradient = super().gradient(x)
        return next_gradient


class Tanh(activations.AbstractTanh):

    """
    TanH activation function widely used for activating inputs in many neural networks.

    Functions
    ----------
    activate
        Function used for activating layer's outputs.

    gradient
        Function calculating gradient needed during backpropagation.
    """

    def activate(
            self,
            x: Union[list, np.ndarray]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        x: list, np.ndarray
            Array of inputs which has to be activated.

        Returns
        --------
        activation: np.ndarray
            Matrix containing activated inputs.
        """

        activation = super().activate(x)
        return activation

    def gradient(
            self,
            x: Union[list, np.ndarray]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        x: list, np.ndarray
            Layer's input which is required for calculating next gradient.

        Returns
        --------
        gradient: np.ndarray
            Matrix containing gradient for another layer.
        """

        gradient = super().gradient(x)
        return gradient


class LeakyRelu(activations.AbstractLeakyRelu):

    """
    LeakyRelu activation function widely used for activating inputs in many neural networks.

    Functions
    ----------
    activate
        Function used for activating layer's outputs.

    gradient
        Function calculating gradient needed during backpropagation.
    """

    def activate(
            self,
            x: Union[list, np.ndarray]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        x: list, np.ndarray
            Array of inputs which has to be activated.

        Returns
        --------
        activation: np.ndarray
            Matrix containing activated inputs.
        """

        activation = super().activate(x)
        return activation

    def gradient(
            self,
            x: Union[list, np.ndarray]
    ) -> np.ndarray:

        """
        Parameters
        -----------
        x: list, np.ndarray
            Layer's input which is required for calculating next gradient.

        Returns
        --------
        gradient: np.ndarray
            Matrix containing gradient for another layer.
        """

        gradient = super().gradient(x)
        return gradient
