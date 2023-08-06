import pytest
from .explanation import AttributionExplanation, ABCExplanation
from ..utils_testing import ctr_eq


def test_attribution_explanation():
    attribution_args_dict = {
        "data": [[1, 2], [3, 4]],
        "values": [[5, 6], [7, 8]],
        "input_shape": [2, 2],
        "output_shape": [],
        "base_value": 0,
        "interaction_order": 0,
        "instance_names": ["r1", "r2"],
        "feature_names": ["f1", "f2"],
        "feature_types": ["continuous", "continuous"],
    }

    attribution_explanation = AttributionExplanation(**attribution_args_dict)
    attribution_sliced = attribution_explanation[:, 1]
    assert attribution_sliced.base_value == 0
    assert ctr_eq(attribution_sliced.data, [2, 4])

    abc_args_dict = attribution_args_dict.copy()
    abc_args_dict["lower_bounds"] = [[0.1, 0.2], [0.3, 0.4]]
    abc_args_dict["upper_bounds"] = [[1.1, 2.2], [3.3, 4.4]]
    abc_explanation = ABCExplanation(**abc_args_dict)

    abc_sliced = abc_explanation[:, 1]
    assert ctr_eq(abc_sliced.lower_bounds, [0.2, 0.4])
