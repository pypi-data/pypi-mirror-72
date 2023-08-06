""" This prototype is not fully documented and is in active development."""

from typing import List, Union, Optional, Any, AnyStr
from .. import SlicerCollection, Slicer


class Explanation:
    pass


# TODO: Re-introduce serialization code.
class AttributionExplanation(Explanation):
    def __init__(
        self,
        # Allow tensor-like objects via Any.
        data: Any,
        values: Any,
        # JSON has no concept of tuples, so we use lists.
        input_shape: List[int],
        output_shape: List[int],
        base_value: Optional[Union[float, List[float]]] = None,
        interaction_order: int = 0,
        instance_names: Optional[List[Any]] = None,
        feature_names: Optional[List[Any]] = None,
        feature_types: Optional[List[AnyStr]] = None,
        **kwargs
    ):
        super().__init__()

        expanded_coordinates = list(
            range(len(input_shape) + interaction_order + len(output_shape))
        )

        data_coordinates = expanded_coordinates[: len(input_shape)]
        values_coordinates = expanded_coordinates
        if len(output_shape) == 0:
            output_coordinates = []
        else:
            output_coordinates = expanded_coordinates[-len(output_shape) :]

        # TODO: Consider having names associated with dimensions in a separate object.
        instance_names_coordinates = [0] if instance_names is not None else []
        feature_names_coordinates = [1] if feature_names is not None else []
        feature_types_coordinates = [1] if feature_types is not None else []

        args_dict = {
            "data": (data_coordinates, data),
            "values": (values_coordinates, values),
            # TODO: Adjust shapes after slicing. For now it's invariant.
            "input_shape": ([], input_shape),
            "output_shape": ([], output_shape),
            "base_value": (output_coordinates, base_value),
            "interaction_order": ([], interaction_order),
            "instance_names": (instance_names_coordinates, instance_names),
            "feature_names": (feature_names_coordinates, feature_names),
            "feature_types": (feature_types_coordinates, feature_types),
        }

        # TODO: Add guard to make sure kwargs are slicer coordinate form.
        for key, value in kwargs.items():
            args_dict[key] = value
        AttributionExplanation._init_slicers(self, **args_dict)

    @staticmethod
    def _init_slicers(obj, **kwargs):
        obj._slicer_collection = SlicerCollection(**kwargs)
        coord_form = SlicerCollection.slicer_coordinate_form(obj._slicer_collection)
        for name, tup in coord_form.items():
            _, slicer = tup
            setattr(obj, name, slicer.o)
        return obj

    @classmethod
    def from_slicers(cls, **kwargs):
        obj = cls.__new__(cls)
        AttributionExplanation._init_slicers(obj, **kwargs)
        return obj

    def __getitem__(self, item):
        new_slicer_collection = self._slicer_collection.__getitem__(item)
        new_slicer_coord_form = SlicerCollection.slicer_coordinate_form(
            new_slicer_collection
        )

        obj = self.__class__.from_slicers(**new_slicer_coord_form)
        return obj


# NOTE: Example specialized explanation (like EBMExplanation).
class ABCExplanation(AttributionExplanation):
    def __init__(
        self,
        data: Any,
        values: Any,
        input_shape: List[int],
        output_shape: List[int],
        base_value: Optional[Union[float, List[float]]] = None,
        interaction_order: int = 0,
        # Instance / features are tabular concepts.
        instance_names: Optional[List[Any]] = None,
        feature_names: Optional[List[Any]] = None,
        feature_types: Optional[List[AnyStr]] = None,
        lower_bounds: Any = None,
        upper_bounds: Any = None,
    ):

        expanded_coordinates = list(
            range(len(input_shape) + interaction_order + len(output_shape))
        )
        lower_bounds_coordinates = expanded_coordinates
        upper_bounds_coordinates = expanded_coordinates
        kwargs_dict = {
            "lower_bounds": (lower_bounds_coordinates, Slicer(lower_bounds)),
            "upper_bounds": (upper_bounds_coordinates, Slicer(upper_bounds)),
        }

        super().__init__(
            data,
            values,
            input_shape,
            output_shape,
            base_value,
            interaction_order,
            instance_names,
            feature_names,
            feature_types,
            **kwargs_dict
        )
