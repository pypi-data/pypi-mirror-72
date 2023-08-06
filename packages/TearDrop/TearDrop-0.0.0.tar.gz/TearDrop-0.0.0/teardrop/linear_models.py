from teardrop.core.abstract_classes._abstract_linear_models import LinearModel
from teardrop.core.regression_output import RegressionResults
from typing import Union
import numpy as np


class LinearRegression(LinearModel):

    def fit(
            self,
            x: Union[list, np.ndarray],
            y: Union[list, np.ndarray]
    ) -> RegressionResults:

        """
        Parameters
        -----------
        x: array-like
            The array containing data about x-axis used for fitting.

        y: array-like
            The array containing data about y-axis used for fitting.

        Returns
        ---------
        reg: RegressionOutput object
            Object containing coefficients used for predicting and checking accuracy.

        See also
        ---------
        teardrop.core.basic_linear_model.RegressionOutput
        """

        reg = super().fit(x, y)
        return reg
