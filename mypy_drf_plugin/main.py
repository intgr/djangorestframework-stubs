from collections.abc import Callable
from functools import partial

from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext, FunctionContext, Plugin
from mypy.types import Type
from typing_extensions import override

from mypy_drf_plugin.lib import fullnames, helpers
from mypy_drf_plugin.transformers import serializers


def transform_serializer_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.BASE_SERIALIZER_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        helpers.get_drf_metadata(sym.node)["serializer_bases"][ctx.cls.fullname] = 1

    serializers.make_meta_nested_class_inherit_from_any(ctx)


class NewSemanalDRFPlugin(Plugin):
    def _get_currently_defined_serializers(self) -> dict[str, int]:
        base_serializer_sym = self.lookup_fully_qualified(fullnames.BASE_SERIALIZER_FULLNAME)
        if base_serializer_sym is not None and isinstance(base_serializer_sym.node, TypeInfo):
            serializer_bases: dict[str, int] = base_serializer_sym.node.metadata.setdefault("drf", {}).setdefault(
                "serializer_bases", {fullnames.BASE_SERIALIZER_FULLNAME: 1}
            )
            return serializer_bases
        return {}

    @override
    def get_base_class_hook(self, fullname: str) -> Callable[[ClassDefContext], None] | None:
        if fullname in self._get_currently_defined_serializers():
            return transform_serializer_class
        return None

    @override
    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname in self._get_currently_defined_serializers():
            list_serializer = self.lookup_fully_qualified(fullnames.LIST_SERIALIZER_FULLNAME)
            if list_serializer is not None and isinstance(list_serializer.node, TypeInfo):
                return partial(serializers.infer_serializer_constructor_return, list_serializer=list_serializer.node)
        return None


def plugin(version: str) -> type[NewSemanalDRFPlugin]:
    return NewSemanalDRFPlugin
