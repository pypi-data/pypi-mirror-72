from . import Slicer, SlicerCollection
import pytest
import pandas as pd
import torch
import numpy as np
from .utils_testing import ctr_eq


def test_pandas():
    dict = {"A": [1, 2], "B": [3, 4], "C": [5, 6]}
    df = pd.DataFrame(dict)

    slicer = Slicer(df)
    assert slicer[0, "A"] == 1
    assert ctr_eq(slicer[:, "A"], [1, 2])
    assert ctr_eq(slicer[0, :], [1, 3, 5])

    df = pd.DataFrame(dict, index=["X", "Y"])
    slicer = Slicer(df)
    assert slicer["X", "A"] == 1
    assert slicer[0, "A"] == 1
    assert slicer[0, 0] == 1
    slicer = Slicer(df["A"])
    assert slicer["X"] == 1
    assert slicer[0] == 1
    assert ctr_eq(slicer[:], [1, 2])

    slicer = Slicer(df, aliases=None)
    with pytest.raises(ValueError):
        _ = slicer["X", "A"]
        _ = slicer[0, "A"]
    assert slicer[0, 0] == 1


def test_alias_passthru():
    dict = {"Harsha": [1, 2], "Sam": [3, 4], "Scott": [5, 6]}
    aliases = {1: ["Age", "Height"]}
    slicer = Slicer(dict, aliases=aliases)
    assert slicer["Harsha", 0] == 1
    assert slicer["Sam", "Height"] == 4


def test_aliasing_slicer():
    array = np.array([[1, 2], [3, 4], [5, 6]])
    dict = {0: [1, 2], 1: [3, 4], 2: [5, 6]}
    containers = [array, dict]
    dict_aliases = {0: ["Harsha", "Sam", "Scott"], 1: ["Age", "Height"]}
    list_aliases = [["Harsha", "Sam", "Scott"], ["Age", "Height"]]
    aliases_types = [dict_aliases, list_aliases]
    for ctr in containers:
        for aliases in aliases_types:
            slicer = Slicer(ctr, aliases=aliases)
            assert slicer.aliases[0][2] == "Scott"
            assert slicer.alias_to_index[1]["Height"] == 1

            assert slicer["Harsha", "Age"] == 1
            assert slicer["Sam", "Height"] == 4


def test_same_coord_slicer_collection():
    arrays = [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 11], [12, 13]]]

    slicer_collection = SlicerCollection(
        ar_first=([0, 1], arrays[0]),
        ar_second=([0, 1], arrays[1]),
        ar_third=([0, 1], arrays[2]),
    )

    assert ctr_eq(slicer_collection[0].ar_first, Slicer(arrays[0])[0])
    assert ctr_eq(slicer_collection[0].ar_second, Slicer(arrays[1])[0])
    assert ctr_eq(slicer_collection[0].ar_third, Slicer(arrays[2])[0])

    assert ctr_eq(slicer_collection[:, 1].ar_first, Slicer(arrays[0])[:, 1])
    assert ctr_eq(slicer_collection[:, 1].ar_second, Slicer(arrays[1])[:, 1])
    assert ctr_eq(slicer_collection[:, 1].ar_third, Slicer(arrays[2])[:, 1])


def test_example_coord_slicer_collection():
    data = [[1, 2], [3, 4]]
    values = [[5, 6], [7, 8]]
    feature_names = ["f1", "f2"]
    instance_names = ["r1", "r2"]
    interaction_order = 0

    slicer_collection = SlicerCollection(
        data=([0, 1], data),
        values=([0, 1], values),
        feature_names=([1], feature_names),
        instance_names=([0], instance_names),
        interaction_order=([], interaction_order),
    )

    actual = slicer_collection[..., 1]
    assert actual.data == [2, 4]
    assert actual.feature_names == "f2"
    assert actual.instance_names == ["r1", "r2"]
    assert actual.interaction_order == 0
    assert actual.values == [6, 8]

    actual = slicer_collection[[0, 1], 1]
    assert actual.data == [2, 4]
    assert actual.feature_names == "f2"
    assert actual.instance_names == ["r1", "r2"]
    assert actual.interaction_order == 0
    assert actual.values == [6, 8]


def test_example_aliases_slicer_collection():
    data = [[1, 2], [3, 4]]
    values = [[5, 6], [7, 8]]
    feature_names = ["f1", "f2"]
    instance_names = ["r1", "r2"]
    interaction_order = 0

    slicer_collection = SlicerCollection(
        data=([0, 1], data),
        values=([0, 1], values),
        feature_names=([1], feature_names, True),
        instance_names=([0], instance_names, True),
        interaction_order=([], interaction_order),
    )

    actual = slicer_collection[..., 1]
    assert actual.data == [2, 4]
    assert actual.feature_names == "f2"
    assert actual.instance_names == ["r1", "r2"]
    assert actual.interaction_order == 0
    assert actual.values == [6, 8]

    actual = slicer_collection["r1", "f2"]
    assert actual.data == 2
    assert actual.feature_names == "f2"
    assert actual.values == 6

    actual = slicer_collection[["r1", "r2"], "f2"]
    assert actual.data == [2, 4]
    assert actual.feature_names == "f2"
    assert actual.instance_names == ["r1", "r2"]
    assert actual.interaction_order == 0
    assert actual.values == [6, 8]


def test_handle_newaxis_ellipses():
    index_tup = (1,)
    max_dim = 3

    expanded_index_tup = Slicer.handle_newaxis_ellipses(index_tup, max_dim)
    assert expanded_index_tup == (1, slice(None), slice(None))


def test_fixed_2d():
    elements = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    li = elements
    df = pd.DataFrame(elements, columns=["A", "B", "C"])

    containers = [li, df]
    for _, ctr in enumerate(containers):
        slicer = Slicer(ctr)

        assert ctr_eq(slicer[0], elements[0])

        # Ranged slicing
        if not isinstance(ctr, dict):
            assert ctr_eq(slicer[-1], elements[-1])
            assert ctr_eq(slicer[0, 0:3:2], elements[0][0:3:2])

        # Array
        assert ctr_eq(slicer[[0, 1, 2], :], elements)

        # All
        assert ctr_eq(slicer[:], elements)
        assert ctr_eq(slicer[tuple()], elements)

        assert ctr_eq(slicer[:, 0], [elements[i][0] for i, _ in enumerate(elements)])
        assert ctr_eq(slicer[[0, 1], 0], [elements[i][0] for i in [0, 1]])
        assert ctr_eq(slicer[[0, 1], 1], [elements[i][1] for i in [0, 1]])
        assert ctr_eq(slicer[0, :], elements[0])
        assert ctr_eq(slicer[0, 1], elements[0][1])

        assert ctr_eq(slicer[..., 0], [elements[i][0] for i, _ in enumerate(elements)])


def test_fixed_1d():
    elements = [1, 2, 3, 4]
    li = elements
    tup = tuple(elements)
    di = {i: x for i, x in enumerate(elements)}
    series = pd.Series(elements)
    array = np.array(elements)
    torch_array = torch.tensor(elements)
    containers = [li, tup, array, torch_array, di, series]
    for _, ctr in enumerate(containers):
        slicer = Slicer(ctr)

        assert ctr_eq(slicer[0], elements[0])

        # Array
        assert ctr_eq(slicer[[0, 1, 2, 3]], elements)
        assert ctr_eq(slicer[[0, 1, 2]], elements[:-1])

        # All
        assert ctr_eq(slicer[:], elements[:])
        assert ctr_eq(slicer[tuple()], elements)

        # Ranged slicing
        if not isinstance(ctr, dict):  # Do not test on dictionaries.
            assert ctr_eq(slicer[-1], elements[-1])
            assert ctr_eq(slicer[0:3:2], elements[0:3:2])


def test_fixed_3d():
    # 3-dimensional fixed dimension case
    elements = [
        [[1, 2, 3], [4, 5, 6]],
        [[7, 8, 9], [10, 11, 12]],
        [[13, 14, 15], [16, 17, 18]],
    ]
    tuple_elements = (
        ((1, 2, 3), (4, 5, 6)),
        ((7, 8, 9), (10, 11, 12)),
        ((13, 14, 15), (16, 17, 18)),
    )
    torch_array = torch.tensor(elements)
    multi_array = np.array(elements)
    list_of_lists = elements
    tuples_of_tuples = tuple_elements
    list_of_multi_arrays = [
        np.array(elements[0]),
        np.array(elements[1]),
        np.array(elements[2]),
    ]
    di_of_multi_arrays = {
        0: np.array(elements[0]),
        1: np.array(elements[1]),
        2: np.array(elements[2]),
    }

    containers = [
        torch_array,
        multi_array,
        tuples_of_tuples,
        list_of_lists,
        list_of_multi_arrays,
        di_of_multi_arrays,
    ]
    for _, ctr in enumerate(containers):
        slicer = Slicer(ctr)

        assert ctr_eq(slicer[0], elements[0])

        # Ranged slicing
        if not isinstance(ctr, dict):
            assert ctr_eq(slicer[-1], elements[-1])
            assert ctr_eq(slicer[0, 0:3:2], elements[0][0:3:2])

        # Array
        assert ctr_eq(slicer[[0, 1, 2], :], elements)

        # All
        assert ctr_eq(slicer[:], elements)
        assert ctr_eq(slicer[tuple()], elements)

        assert ctr_eq(slicer[:, 0], [elements[i][0] for i, _ in enumerate(elements)])
        assert ctr_eq(slicer[[0, 1], 0], [elements[i][0] for i in [0, 1]])
        assert ctr_eq(slicer[[0, 1], 1], [elements[i][1] for i in [0, 1]])
        assert ctr_eq(slicer[0, :], elements[0])
        assert ctr_eq(slicer[0, 1], elements[0][1])

        rows = []
        for i, _ in enumerate(elements):
            cols = []
            for j, _ in enumerate(elements[i]):
                cols.append(elements[i][j][1])
            rows.append(cols)
        assert ctr_eq(slicer[..., 1], rows)
        assert ctr_eq(
            slicer[0, ..., 1], [elements[0][i][1] for i in range(len(elements[0]))]
        )
