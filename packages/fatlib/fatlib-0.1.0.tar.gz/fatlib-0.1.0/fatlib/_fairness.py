from collections import Counter

import numpy as np
import pandas as pd
from aif360.sklearn.metrics import base_rate
from aif360.sklearn.utils import check_groups
from sklearn.utils import Bunch

from ._utils import extract_categorical

__all__ = ["extract_fairness", "set_prot_attr"]


def _get_ref_group_value(rates, ref_group):
    idx = -1 if ref_group == "max" else 0
    ref_group, ref_value = sorted(rates.items(), key=lambda x: x[1])[idx]
    return ref_group, ref_value


def _extract_feature_fairness(X, y, prot_attr, pos_label, ref_group):
    eps = np.finfo(float).eps
    groups, prot_attrs = check_groups(X, prot_attr=prot_attr)
    groups = list(set(groups))
    rates = Bunch()
    for group in groups:
        idx = X[prot_attr] == group
        ret = base_rate(y[idx], pos_label=pos_label)
        rates[group] = ret

    ref_group, ref_value = _get_ref_group_value(rates, ref_group)

    # Calculate the metrics against all.
    idx = X[prot_attr] != ref_group
    rates["__all__"] = base_rate(y[idx], pos_label=pos_label)

    # Devide by a small number if the ref_group is the one with the minimum rate
    # and is zero.
    disparities = Bunch(
        **{k: (v / ref_value) if ref_value else v / eps for k, v in rates.items()}
    )

    bias = Bunch(**{k: not 1.2 > v > 0.8 for k, v in disparities.items()})

    return Bunch(
        ref_group=ref_group,
        rates=rates,
        disparities=disparities,
        bias=bias,
        pos_label=pos_label,
    )


def extract_fairness(X, y, prot_attr=None, pos_label=None, ref_group="max"):
    # Consider the minority class if pos_label is None.
    pos_label = Counter(y).most_common()[-1][0] if pos_label is None else pos_label
    # Consider all the categorical features if prot_attr is not provided.
    prot_attrs = extract_categorical(X)[2] if prot_attr is None else prot_attr
    # Set the indexes
    X, y = set_prot_attr(X, y, prot_attrs)
    ret = Bunch()
    for prot_attr in prot_attrs:
        ret[prot_attr] = _extract_feature_fairness(
            X, y, prot_attr, pos_label, ref_group
        )

    return ret


def set_prot_attr(X, y, prot_attr=None, inplace=False):
    X = pd.DataFrame(X)
    *_, names = extract_categorical(X)
    prot_attr = names if prot_attr is None else prot_attr
    prot_attr = prot_attr if isinstance(prot_attr, list) else [prot_attr]
    given_attrs = set(list(prot_attr))
    existing_attrs = set(names)
    diff = given_attrs - existing_attrs

    if len(diff) > 0:
        msg = (
            f"{diff} are not a categorical attributes. "
            f"Valid attributes are {existing_attrs}"
        )
        raise ValueError(msg)
    X = X.set_index(list(given_attrs), drop=False, inplace=inplace)
    y.index = X.index
    return X, y
