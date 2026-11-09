from mypy.maptype import map_instance_to_supertype
from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext, FunctionContext
from mypy.typeops import make_simplified_union
from mypy.types import Instance, LiteralType, Type, get_proper_type
from mypy_django_plugin.lib import helpers as mypy_django_helpers

from mypy_drf_plugin.lib import fullnames


def infer_serializer_constructor_return(ctx: FunctionContext, *, list_serializer: TypeInfo) -> Type:
    """Restore the inherited __new__ return type when mypy selects a subclass's __init__."""
    serializer = get_proper_type(ctx.default_return_type)
    if not isinstance(serializer, Instance):
        return ctx.default_return_type

    # Only DRF's allocator wraps many=True; a custom __new__ can return something else.
    allocator = next(base for base in serializer.type.mro if "__new__" in base.names)
    if allocator.fullname not in (fullnames.BASE_SERIALIZER_FULLNAME, fullnames.MODEL_SERIALIZER_FULLNAME):
        return ctx.default_return_type

    for names, types in zip(ctx.arg_names, ctx.arg_types, strict=True):
        for name, arg_type in zip(names, types, strict=True):
            if name != "many":
                continue
            many = get_proper_type(arg_type)
            if isinstance(many, Instance) and many.last_known_value is not None:
                many = many.last_known_value
            if isinstance(many, LiteralType):
                if many.value is not True:
                    return ctx.default_return_type
            elif not isinstance(many, Instance) or many.type.fullname != "builtins.bool":
                return ctx.default_return_type

            base = next(base for base in serializer.type.mro if base.fullname == fullnames.BASE_SERIALIZER_FULLNAME)
            instance_type = map_instance_to_supertype(serializer, base).args[0]
            list_type = Instance(list_serializer, [instance_type])
            if isinstance(many, LiteralType):
                return list_type
            return make_simplified_union([serializer, list_type])
    return ctx.default_return_type


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = mypy_django_helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True
