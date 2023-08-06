from teardrop.core.training import Model
import numpy as np
from typing import Union, Optional
from teardrop.layers.core import Dense


class Sequential(Model):
    # TODO: Implement C++ version of NeuralNetwork class for better performance.

    """Neural model used for performing various deep learning tasks.


    NeuralNetwork class for performing deep learning. To perform deep learning you have to add layers (min. 1)
    to the network using ``.add()`` function and passing proper layer type.

    Example
    ---------
    Example of importing and usage of the model.

    >>> import teardrop.neural_models.Sequential as Sequential
    >>> from teardrop.layers.core import Dense
    >>> model = Sequential()
    >>> model.add(Dense(2, activation='sigmoid', input_shape=2))
    >>> model.fit(x, y, n_epochs=5000)


    Functions
    ----------
    fit
        Used for performing model fitting on specified data.

    predict
        Used for making model predict after fitting based on passed data.

    add
        Function used to add layers to the network required for deep learning.

    initialize
        Function used for initializing weights and biases for network.
        You don't have to use it as weights and biases are automatically initialized during fitting!

    history
        Returns the history of losses after fitting.
    """

    def fit(
            self,
            x: Union[np.ndarray, list],
            y: Union[np.ndarray, list],
            learning_rate: Union[float, int] = 0.01,
            n_epochs: int = 5000,
            batch_size: int = 1
    ):

        """
        Network class function used for fitting data into the model allowing it
        to predict values.

        Parameters
        -----------
        x: array-like
            Data used for model fitting.

        y: array-like
            Correct predictions for the model to perform back propagation.

        learning_rate: float or int, optional
            Learning rate deciding how big the gradient step is.

        n_epochs: int, optional
            Number of times network will be trained on `x` data.

        batch_size: int, optional
            Number of data samples in one batch.

        Returns
        --------
        None
        """

        super().fit(x, y, learning_rate, n_epochs, batch_size)

    def predict(self, x: Union[np.ndarray, list]):

        """
        Network class function used to make predicts based on the value passed
        in `x` argument.

        Parameters
        -----------
        x: array-like
            Matrix containing data for predicting.

        Returns
        --------
        prediction: array-like or float
            Prediction made by model on `x` data.
        """

        output = super().predict(x)
        return output

    def add(self, layer: Dense):

        """Network class function used for adding layers to the network.

        NeuralNetwork class function used for adding next layers to the network. Without layers network
        cannot perform fitting and predicting. For

        Parameters
        -----------
        layer
            Layer added to the network.

        Returns
        --------
        None

        See also
        ---------
        teardrop.layers
        """

        super().add(layer)

    def initialize(self, x: Union[np.ndarray, list]):

        """
        Function which initializes the weights and biases for the network.
        Initializing is not required as it's automatically done before after adding new neurons!

        Parameters
        -----------
        x: array-like
            Data matrix which's shape is used for initializing weights.

        Returns
        --------
        None
        """

        super().initialize(x)

    def history(self):

        """
        Function which is used to get the loss history to create various graphs.

        Returns
        --------
        self.loss_history: list
            List containing los for every epoch after fitting.
        """

        return self.loss_history

    def evaluate(
            self,
            x: Union[list, np.ndarray],
            y: Union[list, np.ndarray],
            threshold: Optional[Union[int, float]] = 0.9,
            evaluation_type: str = 'accuracy'
    ):

        """
        Function used for evaluating model's accuracy.

        Parameters
        -----------
        x: array-like
            Data matrix used for performing forward propagation and evaluating.

        y: array-like
            Data matrix containing correct predictions for the network to check
            if predictions are correct.

        threshold: float or int
            The threshold which model's prediction has to pass to be considered good.

        evaluation_type: str
            Type of the evaluation which model will use to evaluate.
            These types are available:
                * accuracy
        """

        result = super().evaluate(x, y, threshold, type)
        return result

    def summary(self):

        """
        Summary function for Sequential model.
        """

        text = super().summary()
        return text