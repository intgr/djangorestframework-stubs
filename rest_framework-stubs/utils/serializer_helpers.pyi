from collections import OrderedDict
from typing import Any, Dict, Iterator, List, MutableMapping, Tuple

from rest_framework.exceptions import ErrorDetail
from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer

class ReturnDict(OrderedDict):
    serializer: BaseSerializer
    def __init__(self, serializer: BaseSerializer = ..., *args, **kwargs): ...
    def copy(self) -> ReturnDict: ...
    def __reduce__(self) -> Tuple[dict, Tuple[dict]]: ...

class ReturnList(list):
    serializer: BaseSerializer
    def __init__(self, serializer: BaseSerializer = ..., *args, **kwargs): ...
    def __reduce__(self) -> Tuple[dict, Tuple[dict]]: ...

class BoundField:
    """
    A field object that also includes `.value` and `.error` properties.
    Returned when iterating over a serializer instance,
    providing an API similar to Django forms and form fields.
    """

    value: Any
    fields: Dict[str, Field]
    errors: List[ErrorDetail]
    def __init__(self, field: Field, value: Any, errors: List[ErrorDetail], prefix: str = ...): ...
    def __getattr__(self, attr_name: str) -> Any: ...
    def as_form_field(self) -> BoundField: ...

class JSONBoundField(BoundField): ...

class NestedBoundField(BoundField):
    def __iter__(self) -> Iterator[str]: ...
    def __getitem__(self, key: str) -> BoundField | NestedBoundField: ...

class BindingDict(MutableMapping[str, Field]):
    serializer: BaseSerializer
    fields: OrderedDict[str, Field]
    def __init__(self, serializer: BaseSerializer): ...
    def __setitem__(self, key: str, field: Field) -> None: ...
    def __getitem__(self, key: str) -> Field: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[Field]: ...  # type: ignore[override]
    def __len__(self) -> int: ...
