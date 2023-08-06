import numpy as np
import pandas as pd
import pytest

import fatlib

data_list = [[0.0, 0, "0"], [1.1, 1, "1"]]
data_df = pd.DataFrame(data_list)


def fit_transformer(X):
    return fatlib.Transformer().fit(X)


@pytest.mark.parametrize("data", [data_list, data_df])
def test_transformer_fit(data):
    transformer = fit_transformer(data)

    assert getattr(transformer, "encoder_", False)
    np.array_equal(transformer.categorical_indices_, [2])
    np.array_equal(transformer.feature_names_, [0, 1, 2])


@pytest.mark.parametrize("data", [data_list, data_df])
def test_transformer_transform(data):

    transformer = fit_transformer(data)
    transformed_data = transformer.transform(data)

    data_expected = [[0.0, 0.0, 0.0], [1.1, 1.0, 1.0]]
    data_transformed = transformed_data.values.tolist()
    np.array_equal(data_transformed, data_expected)

    dtypes_transformed = transformed_data.dtypes
    dtyped_expected = [np.float64, np.int64, np.int64]
    np.array_equal(dtypes_transformed, dtyped_expected)


@pytest.mark.parametrize("data", [data_list, data_df])
def test_transformer_inverse_transform(data):
    transformer = fit_transformer(data)
    transformed_data = transformer.transform(data)
    inversed_data = transformer.inverse_transform(transformed_data)

    inversed_list = inversed_data.values.tolist()
    np.array_equal(inversed_list, data)

    dtypes_transformed = inversed_data.dtypes
    dtyped_expected = [np.float64, np.int64, np.object]
    np.array_equal(dtypes_transformed, dtyped_expected)
