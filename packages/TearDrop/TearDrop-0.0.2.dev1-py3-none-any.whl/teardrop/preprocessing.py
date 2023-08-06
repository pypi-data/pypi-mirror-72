import numpy as np
from typing import Union, Optional


def batch_iterator(
        x: Union[list, np.ndarray],
        y: Optional[Union[list, np.ndarray]] = None,
        batch_size: Optional[int] = 1
        ):

    samples = x.shape[0]
    for i in np.arange(0, samples, batch_size):
        begin = i
        end = min(i + batch_size, samples)

        if y is not None:
            yield x[begin:end], y[begin:end]

        else:
            yield x[begin:end]
