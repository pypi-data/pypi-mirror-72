import numpy as np
import pandas as pd
from sklearn import base, preprocessing

from ._utils import extract_categorical

__all__ = ["Transformer"]


class Transformer(base.BaseEstimator, base.TransformerMixin):
    """Common data transformer for tabular datasets."""

    def fit(self, X, y=None):
        X = self._check_data(X)
        self.feature_names_ = list(X.columns)

        idx, *_ = extract_categorical(X)
        self.categorical_indices_ = idx

        self.encoder_ = preprocessing.OrdinalEncoder(categories="auto", dtype=np.int64)
        self.encoder_.fit(self._get_categorical_subset(X))

        return self

    def transform(self, X):
        return self._transform(X)

    def inverse_transform(self, X):
        return self._transform(X, inverse=True)

    def _get_categorical_subset(self, X):
        return X.iloc[:, self.categorical_indices_]

    def _transform(self, X, inverse=False):
        X = self._check_data(X)
        encoder = self.encoder_
        transform = encoder.inverse_transform if inverse else encoder.transform
        X.iloc[:, self.categorical_indices_] = transform(
            self._get_categorical_subset(X)
        )
        return X

    def _check_data(self, X, feature_names=None):
        data = (
            pd.DataFrame(X)
            if feature_names is None
            else pd.DataFrame(X, columns=feature_names)
        )
        return data.copy()
