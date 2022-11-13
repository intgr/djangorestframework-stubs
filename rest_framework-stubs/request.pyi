from contextlib import contextmanager
from types import TracebackType
from typing import Any, ContextManager, Dict, Iterator, Optional, Sequence, Tuple, Type, Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.http.request import _ImmutableQueryDict
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import BaseParser
from rest_framework.versioning import BaseVersioning
from rest_framework.views import APIView

def is_form_media_type(media_type: str) -> bool: ...

class override_method(ContextManager["Request"]):
    def __init__(self, view: APIView, request: Request, method: str): ...
    def __enter__(self) -> Request: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]: ...

class WrappedAttributeError(Exception): ...

@contextmanager
def wrap_attributeerrors() -> Iterator[None]: ...

class Empty: ...

def clone_request(request: Request, method: str) -> Request: ...

class ForcedAuthentication:
    force_user: Optional[Union[AnonymousUser, AbstractBaseUser]]
    force_token: Optional[str]
    def __init__(
        self, force_user: Optional[Union[AnonymousUser, AbstractBaseUser]], force_token: Optional[str]
    ) -> None: ...
    def authenticate(
        self, request: Request
    ) -> Tuple[Optional[Union[AnonymousUser, AbstractBaseUser]], Optional[Any]]: ...

class Request(HttpRequest):
    parsers: Optional[Sequence[BaseParser]]
    authenticators: Optional[Sequence[Union[BaseAuthentication, ForcedAuthentication]]]
    negotiator: Optional[BaseContentNegotiation]
    parser_context: Optional[Dict[str, Any]]
    version: Optional[str]
    versioning_scheme: Optional[BaseVersioning]
    _request: HttpRequest
    def __init__(
        self,
        request: HttpRequest,
        parsers: Optional[Sequence[BaseParser]] = ...,
        authenticators: Optional[Sequence[BaseAuthentication]] = ...,
        negotiator: Optional[BaseContentNegotiation] = ...,
        parser_context: Optional[Dict[str, Any]] = ...,
    ) -> None: ...
    @property
    def content_type(self) -> str: ...  # type: ignore[override]
    @property
    def stream(self) -> Any: ...
    @property
    def query_params(self) -> _ImmutableQueryDict: ...
    @property
    def data(self) -> Dict[str, Any]: ...
    @property  # type: ignore[override]
    def user(self) -> Union[AbstractBaseUser, AnonymousUser]: ...  # type: ignore[override]
    @user.setter
    def user(self, value: Union[AbstractBaseUser, AnonymousUser]) -> None: ...
    @property
    def auth(self) -> Union[Token, Any]: ...
    @auth.setter
    def auth(self, value: Union[Token, Any]) -> None: ...
    @property
    def successful_authenticator(self) -> Optional[Union[BaseAuthentication, ForcedAuthentication]]: ...
    def __getattr__(self, attr: str) -> Any: ...
    @property
    def DATA(self) -> None: ...
    @property
    def POST(self) -> _ImmutableQueryDict: ...  # type: ignore[override]
    @property
    def FILES(self): ...
    @property
    def QUERY_PARAMS(self) -> None: ...
    def force_plaintext_errors(self, value: Any) -> None: ...
