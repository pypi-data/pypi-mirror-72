from types import FunctionType, MethodType
from typing import Any


class AutoPropertiesDictMeta(type):
    INVALID_TYPES = property, FunctionType, MethodType, classmethod, staticmethod

    def __new__(mcs, name, bases, attrs):
        attrs = mcs._prepare(attrs)
        return super().__new__(mcs, name, bases, attrs)

    @classmethod
    def _check_name(mcs, name: str, value: Any = None) -> bool:
        return (
            bool(name)
            and name.islower()
            and not name.startswith('_')
            and not isinstance(value, mcs.INVALID_TYPES)
        )

    @classmethod
    def _prepare(mcs, attrs: dict) -> dict:
        for name in attrs:
            if mcs._check_name(name, attrs[name]):
                attrs[name] = AutoPropertiesDictMeta.Property(name)
        for name in attrs.get('__annotations__', {}):
            if mcs._check_name(name):
                attrs[name] = AutoPropertiesDictMeta.Property(name)
        return attrs

    class Property:
        __slots__ = 'key',  # pylint: disable=trailing-comma-tuple

        def __init__(self, key=None):
            self.key = key

        def __get__(self, obj, obj_type=None):
            return obj[self.key]

        def __set__(self, obj, value):
            obj[self.key] = value


class AutoPropertiesDict(dict, metaclass=AutoPropertiesDictMeta):
    pass
