from types import ModuleType
from typing import Any, Iterable, List, Optional, Sequence, Tuple, Type, Union

from django.db.models.base import Model
from rest_framework.compat import coreapi
from rest_framework.request import Request
from rest_framework.urlpatterns import _AnyURL
from rest_framework.views import APIView

def common_path(paths: Iterable[str]) -> str: ...
def get_pk_name(model: Type[Model]) -> str: ...
def is_api_view(callback: Any) -> bool: ...

_APIEndpoint = Tuple[str, str, Any]

class EndpointEnumerator:
    patterns: Optional[Sequence[_AnyURL]]
    def __init__(
        self,
        patterns: Optional[Sequence[_AnyURL]] = ...,
        urlconf: Union[str, ModuleType, None] = ...,
    ) -> None: ...
    def get_api_endpoints(
        self, patterns: Optional[Iterable[_AnyURL]] = ..., prefix: str = ...
    ) -> List[_APIEndpoint]: ...
    def get_path_from_regex(self, path_regex: str) -> str: ...
    def should_include_endpoint(self, path: str, callback: Any) -> bool: ...
    def get_allowed_methods(self, callback: Any) -> List[str]: ...

class BaseSchemaGenerator:
    endpoint_inspector_cls: Type[EndpointEnumerator]
    coerce_path_pk: Optional[bool]
    patterns: Optional[Sequence[_AnyURL]]
    urlconf: Optional[str]
    title: Optional[str]
    description: Optional[str]
    version: Optional[str]
    url: Optional[str]
    endpoints: Optional[Sequence[_APIEndpoint]]
    def __init__(
        self,
        title: Optional[str] = ...,
        url: Optional[str] = ...,
        description: Optional[str] = ...,
        patterns: Optional[Sequence[_AnyURL]] = ...,
        urlconf: Optional[str] = ...,
        version: Optional[str] = ...,
    ) -> None: ...
    def create_view(self, callback: Any, method: str, request: Optional[Request] = ...) -> Any: ...
    def coerce_path(self, path: str, method: str, view: APIView) -> str: ...
    def get_schema(self, request: Optional[Request] = ..., public: bool = ...) -> Optional[coreapi.Document]: ...
    def has_view_permissions(self, path: str, method: str, view: APIView) -> bool: ...
