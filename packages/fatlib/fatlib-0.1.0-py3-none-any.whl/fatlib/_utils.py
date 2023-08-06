import numpy as np
import pandas as pd

__all__ = ["atleast_2d", "extract_categorical"]


def atleast_2d(x):
    X = np.atleast_2d(x)
    return pd.DataFrame(X)


def extract_categorical(frame):
    """Extract information about the categorical features of a given
    dataframe."""
    frame = pd.DataFrame(frame)
    dtypes = ["category", "object"]
    idx = np.flatnonzero(frame.dtypes.map(lambda x: x.name in dtypes))
    n = len(idx)
    names = list(frame.columns[idx])
    return idx, n, names
