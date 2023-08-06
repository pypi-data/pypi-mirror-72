from teardrop.core.abstract_classes._abstract_optimizers import AbstractSGD
from typing import Union
import numpy as np


class SGD(AbstractSGD):

    def update(
            self,
            gradient: Union[list, np.ndarray],
            lr: Union[int, float]
    ):
        """
        Parameters
        -----------
        gradient: array-like
            The array with gradient already changed to update weights.

        lr: float/int
            The "length" of the step in updating weights.

        Returns
        --------
        update_size: array-like
            The gradient required for back propagation.
        """

        change = super().update(gradient, lr)
        return change
