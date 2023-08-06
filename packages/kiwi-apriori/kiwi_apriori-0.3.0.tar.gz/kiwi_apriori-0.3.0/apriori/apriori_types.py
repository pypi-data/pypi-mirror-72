from typing import List, Set, Iterable, FrozenSet, Union, Dict

ItemLabel = Union[str, int]
RawTransaction = List[ItemLabel]
SetLike = Union[Set[ItemLabel], FrozenSet[ItemLabel]]
Transaction = FrozenSet[ItemLabel]
