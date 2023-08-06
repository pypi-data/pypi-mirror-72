""" Prototype. This is currently under active development.

TODO:
- Tensorflow
? RELEASE
- Attribution pairs
- Package integration (SHAP, EBM)
? Function evaluation
"""

from typing import Any, AnyStr, Union, List, Tuple, Optional, Dict
from abc import abstractmethod

import numbers

_available_modules = set()


class SlicerCollection:
    """ A coordinated collection of slicers
        that can be sliced jointly across different dimensions.
    """

    def __init__(self, **kwargs):
        """
            Example:
            kwargs = {
                "data": (coordinates, slicer)
                "values": (coordinates, slicer)
                "feature_names": (coordinates, slicer, is_alias)
                "feature_types": (coordinates, slicer)
            }
            SlicerCollection(**kwargs=kwargs)
        """

        self._slicers = {}
        self._coordinates = {}
        self._max_dim = 0
        self._coll_aliases = {}
        for slicer_name, tup in kwargs.items():
            if len(tup) == 2:
                slicer_coordinates, slicer = tup
                is_alias = False
            elif len(tup) == 3:
                slicer_coordinates, slicer, is_alias = tup
            else:  # pragma: no cover
                raise ValueError("Coordinate tuple must be of length 2 or 3.")

            if not isinstance(slicer, Slicer):
                slicer = Slicer(slicer)

            self._slicers[slicer_name] = slicer
            self._coordinates[slicer_name] = slicer_coordinates
            self._max_dim = max(self._max_dim, max(slicer_coordinates, default=-1) + 1)

            if is_alias:
                if len(slicer_coordinates) != 1:
                    raise ValueError("Aliasing only supported on single dimensions.")
                dim = slicer_coordinates[0]
                self._coll_aliases[dim] = slicer_name

            # Create attribute on object corresponding to the slicer's wrapped object.
            setattr(self, slicer_name, slicer.o)

    @staticmethod
    def slicer_coordinate_form(slicer_collection):
        di = {}
        for slicer_name, slicer in slicer_collection._slicers.items():
            slicer_coordinates = slicer_collection._coordinates[slicer_name]
            di[slicer_name] = (slicer_coordinates, slicer)
        return di

    def __repr__(self) -> AnyStr:
        """ Override default repr for human readability.

        Returns:
            String to display.
        """
        return f"{self.__class__.__name__}({str(self.__dict__)})"

    def __getitem__(self, item: Any) -> Any:
        """ Joint slicing into coordinated slicers.
        """

        # Unify slice representation (i.e. expand ellipses).
        item = Slicer.normalize_slice_key(item)
        index_tup = Slicer.handle_newaxis_ellipses(item, self._max_dim)
        aliases = {}
        for dim, slicer_name in self._coll_aliases.items():
            aliases[dim] = self._slicers[slicer_name].o
        _, alias_to_index = Slicer.gen_alias_structures(aliases)
        index_tup = Slicer.handle_aliases(index_tup, alias_to_index)

        # Slice through all objects.
        new_slicer_args = {}
        for slicer_name, slicer_coordinates in self._coordinates.items():
            # If no dimensions, return without slicing.
            if len(slicer_coordinates) == 0:
                new_slicer_args[slicer_name] = (
                    slicer_coordinates,
                    self._slicers[slicer_name],
                )
                continue

            # Resolve indexing to correct coordinates
            index_slicer = Slicer(index_tup, max_dim=1)
            slicer_index = index_slicer[slicer_coordinates]

            # Generate new slicer
            # TODO: More efficient max_dim propagation should be introduced.
            sliced_o = self._slicers[slicer_name][slicer_index]
            aliases = self._slicers[slicer_name].aliases
            sliced_aliases = SlicerCollection._update_slicer_aliases(
                aliases, slicer_index
            )
            new_slicer = Slicer(sliced_o, aliases=sliced_aliases)
            new_coordinates = SlicerCollection._extract_coordinates(
                slicer_index, slicer_coordinates
            )
            new_is_alias = (
                slicer_name in self._coll_aliases.values() and len(new_coordinates) == 1
            )
            new_slicer_args[slicer_name] = (new_coordinates, new_slicer, new_is_alias)

        return self.__class__(**new_slicer_args)

    @staticmethod
    def _update_slicer_aliases(
        aliases: Dict[int, List], slicer_index: Tuple
    ) -> Dict[int, List]:
        new_aliases = {}
        for dim, alias in aliases.items():
            new_aliases[dim] = alias[slicer_index[dim]]

        return new_aliases

    @staticmethod
    def _extract_coordinates(slicer_index: Tuple, slicer_coordinates: List) -> List:
        """ Extracts new coordinates after applying slicing index and maps it back to the original index list. """

        new_slicer_coordinates = []
        for curr_idx, curr_coordinate in zip(slicer_index, slicer_coordinates):
            if not isinstance(curr_idx, int):
                new_slicer_coordinates.append(curr_coordinate)

        return new_slicer_coordinates


class Slicer:
    """ Wrapping object that will unify slicing across data structures.

    What we support:
        Basic indexing (return references):
        - (start:stop:step) slicing
        - support ellipses
        Advanced indexing (return references):
        - integer array indexing
        - boolean array indexing? (discussion for later)

    Numpy Reference:
        Basic indexing (return views):
        - (start:stop:step) slicing
        - support ellipses and newaxis (alias for None)
        Advanced indexing (return copy):
        - integer array indexing, i.e. X[[1,2], [3,4]]
        - boolean array indexing
        - mixed array indexing (has integer array, ellipses, newaxis in same slice)
    """

    def __init__(
        self,
        o: Any,
        aliases: Optional[Union[Dict[int, List], List[List], AnyStr]] = "auto",
        max_dim: Union[None, int, AnyStr] = "auto",
    ):
        """ Provides a consistent slicing API to the object provided.

        Args:
            o: Object to enable consistent slicing.
                Currently supports numpy dense arrays, recursive lists ending with list or numpy.
            aliases: TODO: Fill out later.
            max_dim: Max number of dimensions the wrapped object has.
                If set to "auto", max dimensions will be inferred. This comes at compute cost.
        """
        self.o = o

        # Process indexes
        if aliases == "auto":
            aliases = UnifiedDataHandler.default_alias(o)
        self.aliases, self.alias_to_index = Slicer.gen_alias_structures(aliases)

        # Process max dim
        self.max_dim = max_dim
        if self.max_dim == "auto":
            self.max_dim = UnifiedDataHandler.max_dim(o)

    @staticmethod
    def gen_alias_structures(aliases):
        if aliases is None:
            return {}, {}

        if isinstance(aliases, list):
            aliases = {i: x for i, x in enumerate(aliases)}

        alias_to_index = {}
        for index_dim, index in aliases.items():
            alias_to_index[index_dim] = {x: i for i, x in enumerate(index)}
        return aliases, alias_to_index

    def __repr__(self) -> AnyStr:
        """ Override default repr for human readability.

        Returns:
            String to display.
        """
        return f"{self.__class__.__name__}({self.o.__repr__()})"

    @staticmethod
    def normalize_slice_key(key: Any) -> Tuple:
        """ Normalizes slice key into always being a top-level tuple.

        Args:
            key: Slicing key that is passed within __getitem__.

        Returns:
            A top-level tuple form of the key.
        """
        if not isinstance(key, tuple):
            return (key,)
        else:
            return key

    def __getitem__(self, item: Any) -> Any:
        """ Consistent slicing into wrapped object.

        Args:
            item: Slicing key of type integer or slice.

        Returns:
            Sliced object.

        Raises:
            ValueError: If slicing is not compatible with wrapped object.
        """
        # Turn item into tuple if not already.
        item = Slicer.normalize_slice_key(item)

        # Handle newaxis and ellipses if present.
        index_tup = Slicer.handle_newaxis_ellipses(item, self.max_dim)

        # Handle index names if present.
        index_tup = Slicer.handle_aliases(index_tup, self.alias_to_index)

        # Slice according to object type.
        return UnifiedDataHandler.slice(self.o, index_tup, self.max_dim)

    @staticmethod
    def handle_aliases(
        index_tup: Tuple, alias_to_index: Union[Dict[int, Dict], List[Dict]]
    ) -> Tuple:
        new_index_tup = []

        def resolve(item, dim):
            if isinstance(item, slice):
                return item

            if dim in alias_to_index:
                # NOTE: Don't think about this too hard.
                item = alias_to_index[dim].get(item, item)
            return item

        for dim, item in enumerate(index_tup):
            if isinstance(item, list):
                new_item = []
                for sub_item in item:
                    new_item.append(resolve(sub_item, dim))
            else:
                new_item = resolve(item, dim)
            new_index_tup.append(new_item)

        return tuple(new_index_tup)

    @staticmethod
    def handle_newaxis_ellipses(index_tup: tuple, max_dim: int) -> Tuple:
        """ Expands newaxis and ellipses within a slice for simplification.
        This code is mostly adapted from: https://github.com/clbarnes/h5py_like/blob/master/h5py_like/shape_utils.py#L111

        Args:
            index_tup: Slicing key as a tuple.
            max_dim: Maximum number of dimenions in the respective slicable object.
        
        Returns:
            Expanded slice as a tuple.
        """
        non_indexes = (None, Ellipsis)
        concrete_indices = sum(idx not in non_indexes for idx in index_tup)
        index_list = []
        # newaxis_at = []
        has_ellipsis = False
        int_count = 0
        for item in index_tup:
            if isinstance(item, numbers.Number):
                int_count += 1

            # NOTE: If we need locations of new axis, re-enable this.
            if item is None:
                pass
                # newaxis_at.append(len(index_list) + len(newaxis_at) - int_count)
            elif item == Ellipsis:
                if has_ellipsis:  # pragma: no cover
                    raise IndexError("an index can only have a single ellipsis ('...')")
                has_ellipsis = True
                initial_len = len(index_list)
                while len(index_list) + (concrete_indices - initial_len) < max_dim:
                    index_list.append(slice(None))
            else:
                index_list.append(item)

        if len(index_list) > max_dim:  # pragma: no cover
            raise IndexError("too many indices for array")
        while len(index_list) < max_dim:
            index_list.append(slice(None))

        # return index_list, newaxis_at
        return tuple(index_list)


class BaseHandler:
    @classmethod
    @abstractmethod
    def head_slice(cls, o, index_tup, max_dim):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def tail_slice(cls, o, tail_index, max_dim, flatten=True):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def max_dim(cls, o):
        raise NotImplementedError()

    @classmethod
    def default_alias(cls, o):
        return {}


class SeriesHandler(BaseHandler):
    @classmethod
    def head_slice(cls, o, index_tup, max_dim):
        head_index = index_tup[0]
        is_element = True if isinstance(head_index, int) else False
        sliced_o = o.iloc[head_index]

        return is_element, sliced_o, 1

    @classmethod
    def tail_slice(cls, o, tail_index, max_dim, flatten=True):
        # NOTE: Series only has one dimension,
        #       call slicer again to end the recursion.
        return Slicer(o, max_dim=max_dim)[tail_index]

    @classmethod
    def max_dim(cls, o):
        return len(o.shape)

    @classmethod
    def default_alias(cls, o):
        return {0: o.index.to_list()}


class DataFrameHandler(BaseHandler):
    @classmethod
    def head_slice(cls, o, index_tup, max_dim):
        # NOTE: At head slice, we know there are two fixed dimensions.
        cut_index = index_tup
        is_element = True if isinstance(cut_index[-1], int) else False
        sliced_o = o.iloc[cut_index]

        return is_element, sliced_o, 2

    @classmethod
    def tail_slice(cls, o, tail_index, max_dim, flatten=True):
        # NOTE: Dataframe has fixed dimensions,
        #       call slicer again to end the recursion.
        return Slicer(o, max_dim=max_dim)[tail_index]

    @classmethod
    def max_dim(cls, o):
        return len(o.shape)

    @classmethod
    def default_alias(cls, o):
        return {0: o.index.to_list(), 1: o.columns.to_list()}


class ArrayHandler(BaseHandler):
    @classmethod
    def head_slice(cls, o, index_tup, max_dim):
        # Check if head is string
        head_index, tail_index = index_tup[0], index_tup[1:]
        cut = 1

        for sub_index in tail_index:
            cut += 1
            if isinstance(sub_index, str):
                break

        # Process native array dimensions
        cut_index = index_tup[:cut]
        is_element = True if isinstance(cut_index[-1], int) else False
        sliced_o = o[cut_index]

        return is_element, sliced_o, cut

    @classmethod
    def tail_slice(cls, o, tail_index, max_dim, flatten=True):
        if flatten:
            return Slicer(o, max_dim=max_dim)[tail_index]
        else:
            inner = [Slicer(e, max_dim=max_dim)[tail_index] for e in o]
            if _safe_isinstance(o, "numpy", "ndarray"):
                import numpy

                return numpy.array(inner)
            elif _safe_isinstance(o, "torch", "Tensor"):
                import torch

                if len(inner) > 0 and isinstance(inner[0], torch.Tensor):
                    return torch.stack(inner)
                else:
                    return torch.tensor(inner)
            else:
                raise ValueError(f"Cannot handle type {type(o)}.")  # pragma: no cover

    @classmethod
    def max_dim(cls, o):
        return len(o.shape)


class DictHandler(BaseHandler):
    @classmethod
    def head_slice(cls, o, index_tup, max_dim):
        head_index = index_tup[0]
        if isinstance(head_index, (tuple, list)) and len(index_tup) == 0:
            return False, o, 1

        if isinstance(head_index, (list, tuple)):
            return (
                False,
                {
                    sub_index: Slicer(o, max_dim=max_dim)[sub_index]
                    for sub_index in head_index
                },
                1,
            )
        elif isinstance(head_index, slice):
            if head_index == slice(None, None, None):
                return False, o, 1
            return False, o[head_index], 1
        else:
            return True, o[head_index], 1

    @classmethod
    def tail_slice(cls, o, tail_index, max_dim, flatten=True):
        if flatten:
            return Slicer(o, max_dim=max_dim)[tail_index]
        else:
            return {k: Slicer(e, max_dim=max_dim)[tail_index] for k, e in o.items()}

    @classmethod
    def max_dim(cls, o):
        return max([UnifiedDataHandler.max_dim(x) for x in o.values()], default=-1) + 1


class ListTupleHandler(BaseHandler):
    @classmethod
    def head_slice(cls, o, index_tup, max_dim):
        head_index = index_tup[0]
        if isinstance(head_index, (tuple, list)) and len(index_tup) == 0:
            return False, o, 1

        if isinstance(head_index, (list, tuple)):
            if len(head_index) == 0:
                return False, o, 1
            else:
                results = [
                    Slicer(o, max_dim=max_dim)[sub_index] for sub_index in head_index
                ]
                results = tuple(results) if isinstance(o, tuple) else results
                return False, results, 1
        elif isinstance(head_index, slice):
            return False, o[head_index], 1
        elif isinstance(head_index, int):
            return True, o[head_index], 1
        else:  # pragma: no cover
            raise ValueError(f"Invalid key {head_index} for {o}")

    @classmethod
    def tail_slice(cls, o, tail_index, max_dim, flatten=True):
        if flatten:
            return Slicer(o, max_dim=max_dim)[tail_index]
        else:
            results = [Slicer(e, max_dim=max_dim)[tail_index] for e in o]
            return tuple(results) if isinstance(o, tuple) else results

    @classmethod
    def max_dim(cls, o):
        return max([UnifiedDataHandler.max_dim(x) for x in o], default=-1) + 1


class UnifiedDataHandler:
    """ Registry that maps types to their unified slice calls."""

    """ Class attribute that maps type to their unified slice calls."""
    type_map = {
        ("builtins", "list"): ListTupleHandler,
        ("builtins", "tuple"): ListTupleHandler,
        ("builtins", "dict"): DictHandler,
        ("torch", "Tensor"): ArrayHandler,
        ("numpy", "ndarray"): ArrayHandler,
        ("pandas.core.frame", "DataFrame"): DataFrameHandler,
        ("pandas.core.series", "Series"): SeriesHandler,
    }

    @classmethod
    def slice(cls, o, index_tup, max_dim):
        # NOTE: Unified handles base cases such as empty tuples, which
        #       specialized handlers do not.
        if isinstance(index_tup, (tuple, list)) and len(index_tup) == 0:
            return o

        # Slice as delegated by data handler.
        o_type = _type_name(o)
        head_slice = cls.type_map[o_type].head_slice
        tail_slice = cls.type_map[o_type].tail_slice

        is_element, sliced_o, cut = head_slice(o, index_tup, max_dim)
        out = tail_slice(sliced_o, index_tup[cut:], max_dim - cut, is_element)
        return out

    @classmethod
    def max_dim(cls, o):
        o_type = _type_name(o)
        if o_type not in cls.type_map:
            return 0
        return cls.type_map[o_type].max_dim(o)

    @classmethod
    def default_alias(cls, o):
        o_type = _type_name(o)
        if o_type not in cls.type_map:
            return {}
        return cls.type_map[o_type].default_alias(o)


def _type_name(o: object) -> Tuple[str, str]:
    return o.__class__.__module__, o.__class__.__name__


def _safe_isinstance(o: object, module_name: str, type_name: str) -> bool:
    o_module, o_type = _type_name(o)
    return o_module == module_name and o_type == type_name
