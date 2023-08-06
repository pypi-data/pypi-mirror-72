from .query import Query
from .utils_testing import ctr_eq


def test_func_parse():
    # ### Local explanation for instance 0
    # # For given class 0-1, give me the top 5 abs feature importance
    # _ = e[0, "~top(5)", [0, 1]]
    # # Give biggest feature specific to class 0
    # _ = e[0, "~maxabs()", 0]
    # _ = e[0, :, 0]["!maxabs()"]
    # # Give biggest feature across classes, then give me class 0 value
    # _ = e[0, "!maxabs()", 0]
    # _ = e[0, "~maxabs()"][0]

    data = [-1, 2, -3, 4, 5]
    is_element, func = Query("!top(2, desc=False)").value()
    result = func(data)
    assert is_element == False
    assert ctr_eq(result, [4, 5])


# def test_func_2d_array():
#     data = [[1,2], [3,-4]]
#     is_element, result = Query("maxabs()").eval(data)
#     assert is_element == True
#     assert result == 4


def test_scalar():
    qry = Query("Age")
    assert qry.qry_type == "scalar"
    assert qry.value() == "Age"


def test_func_maxabs():
    data = [-1, 2, -3, 4, 5]
    is_element, func = Query("maxabs()").value()
    result = func(data)
    assert is_element == True
    assert result == 5
