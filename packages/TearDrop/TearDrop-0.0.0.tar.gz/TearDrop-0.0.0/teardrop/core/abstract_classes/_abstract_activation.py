from .base_classes._base_activation import ActivationFunction
import numpy as np


class AbstractSigmoid(ActivationFunction):

    def activate(self, x):
        return np.divide(1, 1 + np.exp(-x))

    def gradient(self, x):
        sig = self.activate(x)
        return np.multiply(sig, 1 - sig)


class AbstractRelu(ActivationFunction):

    def activate(self, x):
        return np.where(x > 0, x, 0)

    def gradient(self, x):
        return np.where(x > 0, 1, 0)


class AbstractSoftmax(ActivationFunction):

    def activate(self, x):
        x -= np.max(x)
        exp = np.exp(x)
        return np.divide(exp, np.sum(exp))

    def gradient(self, x):
        pass
        # TODO: Add gradient for softmax


class AbstractTanh(ActivationFunction):

    def activate(self, x):
        active = np.divide(2, 1 + np.exp(-2*x)) - 1
        return active

    def gradient(self, x):
        gradient = 1 - np.square(self.activate(x))
        return gradient


class AbstractLeakyRelu(ActivationFunction):

    def activate(self, x):
        return np.where(x > 0, x, 0.01 * x)

    def gradient(self, x):
        return np.where(x > 0, x, 0.01 * x)
