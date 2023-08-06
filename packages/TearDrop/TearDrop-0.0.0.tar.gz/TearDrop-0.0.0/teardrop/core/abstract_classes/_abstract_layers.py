import numpy as np
from teardrop.core.abstract_classes.base_classes._base_layer import Layer
from abc import ABCMeta
import teardrop.core.math.activations as math
from typing import Union


class AbstractDenseLayer(Layer, metaclass=ABCMeta):

    def __init__(self, number_of_neurons, activation, input_shape=None):
        self.type = "Dense"
        self.name = None
        self.weights = []
        self.biases = []
        self.layer_input = None
        self.layer_output = None
        self.input_shape = input_shape
        # TODO: Change initializing weights and biases to numpy

        if isinstance(number_of_neurons, int):
            self.neurons = number_of_neurons
        else:
            raise ValueError(f"Number of neurons in layer has to be int, not {type(number_of_neurons)}.")

        if activation == 'sigmoid':
            self.activation = math.Sigmoid()

        elif activation == 'relu':
            self.activation = math.Relu()

        else:
            raise TypeError(f"There is no activation function named {activation} or it hasn't been implemented yet.")

        self.output_shape = (None, self.neurons)

    def _forward(self, x):

        self.layer_input = x
        self.layer_output = np.dot(x, self.weights) + self.biases
        return self.activation.activate(self.layer_output)

    def _backward(self, last_derivative, lr, optimizer):

        w = np.copy(self.weights)

        dfunction = np.multiply(last_derivative, self.activation.gradient(self.layer_output))
        d_w = np.multiply(np.dot(self.layer_input.T, dfunction), (1. / self.layer_input.shape[1]))
        d_b = np.divide(1., self.layer_input.shape[1]) * np.dot(np.ones((self.biases.shape[0], last_derivative.shape[0])),
                                                                dfunction)

        self.weights -= optimizer.update(d_w, lr)
        self.biases -= np.multiply(lr, d_b)

        return np.dot(dfunction, w.T)

    def _initialize(self, neurons):

        self.weights = np.random.rand(neurons, self.neurons) / 100  # dividing by 100 to make it more precise
        self.biases = np.random.rand(1, self.neurons) / 100

    def _name(self, number):
        self.name = f"dense_{number}"


class AbsRNN(Layer, metaclass=ABCMeta):

    def __init__(
            self,
            cells: int,
            learning_rate: Union[int, float]
    ):

        self.type = "RNN"
        self.name = None
        self.lr = learning_rate
        self.cells = cells
        self.weights = []
        self.weightsV = []
        self.biases = []
        self.outputs = {}

    def _forward(
            self,
            x: Union[np.ndarray, list]
    ) -> np.ndarray:

        sig = math.Sigmoid()


        """sigmoid = math.Sigmoid()

        cell_values = list()
        cell_values.append(np.zeros(self.cells))

        # We are creating a dict for storing values passed to the next layer
        passed_hidden_states = {}

        # First hidden state is zero because it's for first RNN neuron which has no previous neurons
        passed_hidden_states[0] = np.zeros(x.shape)

        # We are moving through all cells in layer and calculating their output and hidden state
        for cell_num in range(self.cells):

            # Calculating the hidden state which will be later passed to the next neuron
            # TODO: Check if hidden state and outputs are calculated correctly

            if cell_num == 0:
                weighted_hidden = passed_hidden_states[cell_num] + self.biases[cell_num - 1]

            else:
                weighted_hidden = np.dot(passed_hidden_states[cell_num].T, self.weightsV[cell_num - 1]) + self.biases[
                    cell_num - 1]

            weighted_input = np.dot(x, self.weights)
            hidden_state = sigmoid.activate(weighted_input + weighted_hidden)
            passed_hidden_states[cell_num + 1] = copy.deepcopy(hidden_state)

            self.outputs[cell_num] = copy.deepcopy(hidden_state)
        outputs = np.array(np.array(list(self.outputs.values()))).reshape((1, self.cells))
        return outputs"""

    def _forward_cell(self, x, last_hidden_state):

        tanh = math.Tanh()
        softmax = math.Softmax()

        input_sum = np.dot(x, self.weights)
        hidden_sum = np.dot(last_hidden_state, self.weightsV)
        hidden_tanh = tanh.activate(input_sum + hidden_sum)
        hidden = hidden_tanh + self.biases
        output = softmax.activate(hidden)

        return output, hidden

    def _backward(
            self,
            last_derivative: Union[list, np.ndarray],
            lr: Union[int, float],
            optimizer
    ) -> np.ndarray:

        # We initialize all deltas at 0 matrix and after back propagation we will subtract these from the real weights
        weights_update = np.zeros(self.weights.shape)
        weightsV_update = np.zeros(self.weightsV.shape)
        sig = math.Sigmoid()

        # We are moving through all RNN cells with time step -1
        for cell_num in range(self.cells-1, -1, -1):
            # TODO: Implement time step in BPTT

            """last = np.dot(last_derivative, self.outputs[cell_num])
            grad = sig.gradient(self.outputs[cell_num])
            weights_update += last * grad
            prev_cell = self.outputs[cell_num - 1]
            weightsV_update += np.dot(prev_cell, self.outputs[cell_num])"""

        self.weights -= optimizer.update(weights_update, lr)
        self.weightsV -= optimizer.update(weightsV_update, lr)

        """
        def backward(self, xs, hs, ps, targets):
            # backward pass: compute gradients going backwards
            dU, dW, dV = np.zeros_like(self.U), np.zeros_like(self.W), np.zeros_like(self.V)
            db, dc = np.zeros_like(self.b), np.zeros_like(self.c)
            dhnext = np.zeros_like(hs[0])
            for t in reversed(range(self.seq_length)):
                dy = np.copy(ps[t])
                # through softmax
                dy[targets[t]] -= 1  # backprop into y
                # calculate dV, dc
                dV += np.dot(dy, hs[t].T)
                dc += dc
                # dh includes gradient from two sides, next cell and current output
                dh = np.dot(self.V.T, dy) + dhnext  # backprop into h
                # backprop through tanh non-linearity
                dhrec = (1 - hs[t] * hs[t]) * dh  # dhrec is the term used in many equations
                db += dhrec
                # calculate dU and dW
                dU += np.dot(dhrec, xs[t].T)
                dW += np.dot(dhrec, hs[t - 1].T)
                # pass the gradient from next cell to the next iteration.
                dhnext = np.dot(self.W.T, dhrec)
            # clip to mitigate exploding gradients
            for dparam in [dU, dW, dV, db, dc]:
                np.clip(dparam, -5, 5, out=dparam)
            return dU, dW, dV, db, dc
        """

        return weights_update

    def initialize(
            self,
            cells: int
    ):

        self.weights = np.random.rand(cells, self.cells) / 100
        self.biases = np.random.rand(1, self.cells) / 100
        self.weightsV = np.random.rand(1, self.cells - 1) / 100

    def _name(
            self,
            number: int
    ):
        self.name = f'rnn_{number}'
