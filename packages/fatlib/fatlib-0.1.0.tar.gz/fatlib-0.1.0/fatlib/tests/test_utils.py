import numpy as np
import pytest

import fatlib


def test_atleast_2d():
    array = [1, 1, 1]
    result = fatlib.atleast_2d(array)
    assert np.array_equal(result.shape, [1, 3])

    array = np.array([1, 1, 1])
    result = fatlib.atleast_2d(array)
    assert np.array_equal(result.shape, [1, 3])


@pytest.mark.parametrize(
    "input, expected_idx, expected_n, expected_names",
    [
        ([dict(a=0, b=1, c=2.2)], [], 0, []),
        ([dict(a="0", b="1", c=1.1)], [0, 1], 2, ["a", "b"]),
        ([dict(a="alpha", b="1", c="1.1")], [0, 1, 2], 3, ["a", "b", "c"]),
    ],
)
def test_extra_categorical(input, expected_idx, expected_n, expected_names):
    idx, n, names = fatlib.extract_categorical(input)
    assert np.array_equal(idx, expected_idx)
    assert n == expected_n
    assert np.array_equal(names, expected_names)
